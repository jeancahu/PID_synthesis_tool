#!/usr/bin/env python

import threading
import socket
from subprocess import Popen as subproc
from subprocess import PIPE

# Comunicacion cliente-servidor:
class Client(threading.Thread):
    """ Cliente conectado al server
    """
    def __init__(self, socket_client, datos_cliente):
        threading.Thread.__init__(self)
        self.socket = socket_client
        self.socket.setblocking(True)

        ## Client data
        self.datos_str = datos_cliente[0] + ":" + str(datos_cliente[1])
        self.sha_id = ''
        self.eof = '\n'+"EOF"+'\n'
        print("El cliente " + self.datos_str + " se ha conectado")

        ## Model data
        # var: str: model information and parametes
        self.model = ''
        self.model_flags = {}
        # var: str: model_str <- "FRA_ORDER TIME_CONS PROP_CONS DEAD_TIME"
        self.model_str = ''
        # var: str: Temporals absolute path in system
        self.cach_path = ''
    
    def run(self):
        """ 
        Este hilo se encarga de ejecutar las diferentes transacciones de datos
        necesarias para compartir el modelo o la respuesta del sistema desde
        el cliente al servidor y posteriormente los parámetros del controlador
        y la imagen de la nueva implementación simulada, desde el servidor al
        dispositivo cliente
    
        Primer tramo: Tipo de información: [model,response_file]
        Segundo tramo: Tupla de parámetros o fichero de texto plano según sea
        el caso
        """

        # Receive controller type
        model = self.socket.recv(1024) # Recibe 512 bytes del cliente
        self.model = model.decode() # Decodificar datos según el protocolo
        print("El modelo y parámetros son: ", self.model) # Imprime los datos en la bitácora

        # Flags default definition
        self.model_flags['type'] = 'model_null'                # Default model value
        self.model_flags['concatenate_params_result'] = False  # Concatenate model params to solution
        self.model_flags['no_images'] = False                  # Do not send images
        self.model_flags['simulation_vectors'] = False         # Send simulation result vectors
        self.model_flags['gnuplot'] = False                    # Generate images with GNUplot
        self.model_flags['model_parameters'] = False           # Send model parameters, IDFOM results
        self.model_flags['output_format'] = 'human_readable'   # Send results table with format
        
        # Flags definition
        if 'model_fotf' in self.model:
            self.model_flags['type'] = 'model_fotf'
        if 'model_file' in self.model:
            self.model_flags['type'] = 'model_file'
        if 'concatenate_params_result' in self.model:
            self.model_flags['concatenate_params_result'] = True
        if 'no_images' in self.model:
            self.model_flags['no_images'] = True
        if 'simulation_vectors' in self.model:
            self.model_flags['simulation_vectors'] = True
        if 'gnuplot' in self.model:
            self.model_flags['gnuplot'] = True
        if 'model_parameters' in self.model:
            self.model_flags['model_parameters'] = True
        if 'json_format' in self.model:
            self.model_flags['output_format'] = 'json'
        elif 'm_code_format' in self.model:
            self.model_flags['output_format'] = 'm_code'

        # Resolve model logic
        if self.model_flags['type'] == 'model_fotf':
            # Data model TF processing
            self.model_fotf()
            self.compute_controller_params_and_simulations()
            self.send_controller_parameters()
            if self.model_flags['simulation_vectors']:
                self.send_simulation_vectors()
            if not self.model_flags['no_images']:
                self.send_images()
            if self.model_flags['model_parameters']:
                self.send_model_parameters()

        elif self.model_flags['type'] == 'model_file':
            # Data file processing
            self.model_file()
            self.compute_controller_params_and_simulations()
            self.send_controller_parameters()
            if self.model_flags['simulation_vectors']:
                self.send_simulation_vectors()
            if not self.model_flags['no_images']:
                self.send_images()
            if self.model_flags['model_parameters']:
                self.send_model_parameters()

        else:
            self.model_undefined()

        self.__del__()

    def model_file (self):
        # Se responde al cliente
        response ="model_accepted"+self.eof
        self.socket.send(response.encode())

        # Receive model data vectors as string
        self.step_response = self.receive_plain_text()

    def model_fotf (self):
        # Se responde al cliente
        response ="model_accepted"+self.eof
        self.socket.send(response.encode('utf-8'))

        # Receive model data and erase unnecessary syntax
        data = self.socket.recv(512).decode()
        data = data.replace("\nEOF\n",'')
        data = data.replace('\n',' ')
        self.model_str = data.replace(',',' ')
        print(self.model_str)

    def model_undefined (self):
        # Se responde al cliente
        response ="model_denied"+self.eof
        self.socket.send(response.encode())

    def compute_controller_params_and_simulations (self):
        # Send tuning results
        ## Ejecutar el subprocess
        if self.model_flags['type'] == 'model_fotf':
            command = '../../bash/compute_request.sh '\
                +self.model_flags['output_format']+' '+self.model_str
        elif self.model_flags['type'] == 'model_file':
            command = '../../bash/compute_request.sh '\
                +self.model_flags['output_format']+' << EOF\n'\
                +self.step_response+'\nEOF\n'
        else:
            pass

        tuning_process = subproc(command,
                                  stdout=PIPE,
                                  shell=True)
        out, err = tuning_process.communicate()
        tuning_process.terminate()
        self.cach_path = out.decode().split('\n')[0]
        print(self.cach_path)

    def send_model_parameters (self):
        ## Open IDFOM results file
        file_path = self.cach_path+"/identool_results_json_format.txt"
        results_file = open(file_path)
        results_file = ''.join(results_file.readlines())

        ## Send file content
        self.socket.send(results_file.encode('utf-8'))

        ## Read client ack response
        print(self.socket.recv(512).decode('utf-8'))

    def send_controller_parameters (self):
        ## Open results file
        file_path = self.cach_path+"/results_table.txt"
        results_file = open(file_path)
        results_file = ''.join(results_file.readlines())

        ## Send file content
        result = results_file+self.eof
        self.socket.send(result.encode('utf-8'))

    def send_simulation_vectors (self):
        ## Send images
        command = '../../bash/wait_and_send_vectors.sh '+self.cach_path
        simulation_process = subproc(command,
                                  stdout=PIPE,
                                  shell=True)
        out, err = simulation_process.communicate()
        simulation_process.terminate()
        vectors_str = out.decode()+"\nEOF\n"

        ## Receive client ack
        self.socket.sendall(vectors_str.encode('utf-8'))
        print(self.socket.recv(512).decode('utf-8'))

    def send_images (self):
        ## Send images
        command = '../../bash/wait_and_list_images.sh '+self.cach_path
        simulation_process = subproc(command,
                                  stdout=PIPE,
                                  shell=True)
        out, err = simulation_process.communicate()
        simulation_process.terminate()
        images_str = out.decode()
        images_list = images_str.split(',')
        print(images_list)

        ####
        for image in images_list[1:]:
            print("Enviando nombre de la imagen")
            image_name = image[:-4] + '\n'
            image_name = image_name.encode('utf-8')
            self.socket.send(image_name)

            print("Recibiendo la confirmación del usuario")
            print(self.socket.recv(512).decode())

            with open(self.cach_path+'/'+image, "rb") as imageFile:
                image_hex = imageFile.read()
                self.socket.sendall(image_hex)

        self.socket.send("END".encode('utf-8'))
        ####
        
    def receive_plain_text (self):
        result = ""
        while not 'EOF' in result:
            # Recibe 512 bytes del cliente; data len
            result += self.socket.recv(512).decode()
        return result.replace("\nEOF\n",'')

    def stop(self):
        self._is_running = False

    def __del__(self):
        print("El cliente " + self.datos_str + " se ha desconectado")
        self.socket.close() # El cliente se despide
        self.stop()
