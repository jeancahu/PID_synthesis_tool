from ..rules import frac_order as _frac_order # Only rule it has by now

#import numpy as np
#import matplotlib
#from scipy import signal
#import control
#from oct2py import Oct2py as o2p # ??
from subprocess import Popen, PIPE, STDOUT
from os import path

class FractionalOrderModel():
    def __init__(self,
                 alpha=0,                 # Fractional order   (alpha)
                 time_constant=0,         # Main time constant (T)
                 proportional_constant=0, # Gain               (K)
                 dead_time_constant=0,    # Dead time          (L)

                 time_vector=[], # Time vetor to identify the plant model
                 step_vector=[], # Step vector to identify the plant model
                 resp_vector=[]  # Open-loop system response to identify the plant model
                 ):

        print("Create a fractional order model for the plant")

        ## Identify the plant model
        if not (alpha or time_constant or proportional_constant or dead_time_constant):
            if not (len(time_vector) and len(step_vector) and len(resp_vector)):
                raise ValueError("Plant model wrong input values, no vectors or constants")

            try:
                print(path.join(path.dirname(__file__), '../matlib/'))
                octave_run = Popen(
                    ['octave'],
                    stdout=PIPE,
                    stdin=PIPE,
                    stderr=PIPE,
                    start_new_session=True)

                script = open('IDFOM.m', 'r').readlines()
                script = "".join(script)

                octave_run.stdin.write(script.encode())
                octave_run.stdin.close()

                lines = [ line.decode() for line in octave_run.stdout.readlines()]
                print("".join(lines))

                octave_run.terminate()
                print(octave_run.returncode)
            except Exception as e:
                print(e)
                #raise ValueError("Plant model wrong input values")


        try:
            self.alpha = float(alpha)
            self.T     = float(time_constant)
            self.K     = float(proportional_constant)
            self.L     = float(dead_time_constant)
        except Exception:
            raise ValueError("Plant model wrong input values")

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

    def __str__(self):
        return str(self.toDict())
