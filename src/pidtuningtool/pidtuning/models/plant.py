from ..rules import frac_order as _frac_order # Only rule it has by now

#import numpy as np
#import matplotlib
#from scipy import signal
#import control
#from oct2py import Oct2py as o2p # ??
from subprocess import Popen, PIPE, STDOUT
from os import path, remove, rmdir
import tempfile
import pandas as pd
import json

class FractionalOrderModel():
    def __init__(self,
                 alpha=0,                 # Fractional order   (alpha)
                 time_constant=0,         # Main time constant (T)
                 proportional_constant=0, # Gain               (K)
                 dead_time_constant=0,    # Dead time          (L)

                 time_vector=[], # Time vector to identify the plant model
                 step_vector=[], # Step vector to identify the plant model
                 resp_vector=[]  # Open-loop system response to identify the plant model
                 ):

        ## Identify the plant model
        if (alpha or time_constant or proportional_constant or dead_time_constant):
            try:
                self.alpha = float(alpha)
                self.T     = float(time_constant)
                self.K     = float(proportional_constant)
                self.L     = float(dead_time_constant)
                self.IAE   = 0.0
            except Exception:
                raise ValueError("Plant model wrong input values")

        else:
            if not (len(time_vector) and len(step_vector) and len(resp_vector)):
                raise ValueError("Plant model wrong input values, no vectors or constants")

            try:
                octalib_path = path.join(path.dirname(__file__), '../octalib/')
                octave_run = Popen(
                    ['octave-cli'],
                    cwd=octalib_path,
                    stdout=PIPE,
                    stdin=PIPE,
                    stderr=PIPE,
                    start_new_session=True)

                tmpdir = tempfile.mkdtemp()
                results_file = path.join(tmpdir, 'results.json')
                step_response_file = path.join(tmpdir, 'model_vs_initial_step_response.csv')

                script = open(path.join(octalib_path, 'IDFOM.m'), 'r').readlines()
                script = """
                % Run on execution start
version_info=ver("MATLAB");

try
  if (version_info.Name=="MATLAB")
    fprintf("Running on Matlab\\n")
  end
catch ME
  fprintf("Running on Octave\\n")
  %% Octave load packages
  pkg load control
  pkg load symbolic
  pkg load optim
end

fprintf("Running initial module\\n")

%clc;
clear;

%% Define
s=tf('s');

file_json_id = fopen("{}", "wt");
fid=fopen("{}",'wt');

%% Global variables definition
global To vo Lo Ko ynorm unorm tnorm long tin tmax tu

%% Load data from thread cache
in_v1={};                                % time vector
in_v2={};                                % control signal vector
in_v3={};                                % controled variable vector

                """.format(
                    results_file,
                    step_response_file,
                    str(time_vector).replace(',',';'),
                    str(step_vector).replace(',',';'),
                    str(resp_vector).replace(',',';'),
                ) + "".join(script)

                octave_run.stdin.write(script.encode())
                octave_run.stdin.close()

                ### The two next lines will wait till the program ends. !IMPORTANT
                lines = [ line.decode() for line in octave_run.stdout.readlines()]
                lines = [ line.decode() for line in octave_run.stderr.readlines()]

                if octave_run.terminate():
                    raise Exception("Internal Octave/Matlab execution error")

                results = open(results_file, 'r')
                results_dict = json.loads("".join(results.readlines()))
                results.close()


                colums = ["time", "step", "initial", "model"]
                df = pd.read_csv(step_response_file, sep='\t', header=None, names=colums)

                self.time_vector=df.time.tolist()        # Time vector
                self.step_vector=df.step.tolist()        # Step vector
                self.resp_vector=df.initial.tolist()      # Open-loop system response
                self.model_resp_vector=df.model.tolist()  # Open-loop model-system response

                remove(step_response_file)
                remove(results_file)
                rmdir(tmpdir)

                ## Computed params
                self.alpha = results_dict["v"]
                self.T = results_dict["T"]
                self.K = results_dict["K"]
                self.L = results_dict["L"]
                self.IAE = results_dict["L"]

            except Exception as e:
                print(e)
                raise ValueError("Plant response wrong input vectors, verify your data")

        ## Tune controllers
        self.controllers = self.tune_controllers()

    def tune_controllers(self):
        controllers = []
        for ctype in _frac_order.valid_controllers:
            for Ms in _frac_order.valid_Ms:
                temp = _frac_order.tuning(self.alpha, self.T, self.K, self.L, Ms, ctype)
                if temp:
                    controllers.append(temp)
        return controllers

    def toDict(self):
        return {
            'alpha' : self.alpha,
            'T'     :     self.T,
            'K'     :     self.K,
            'L'     :     self.L
        }

    def toResponse(self):
        return {
            'time'    :   self.time_vector,       # Time vector
            'step'    :   self.step_vector,       # Step vector
            'respo'   :   self.resp_vector,       # Open-loop system response
            'm_respo' :   self.model_resp_vector  # Open-loop model-system response
        }

    def __str__(self):
        return str(self.toDict())
