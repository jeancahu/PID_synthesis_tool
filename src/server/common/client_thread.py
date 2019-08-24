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
        # var: str: model type
        self.model_type = ''        
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
        model = self.socket.recv(512) # Recibe 512 bytes del cliente
        self.model_type = model.decode()[:10] # Decodificar datos según el protocolo
        print("El modelo es de tipo: ", self.model_type) # Imprime los datos en la bitácora
  
        if self.model_type == 'model_fotf':
            # Data model processing
            self.model_fotf()
            self.compute_controller_params_and_simulations()
            self.send_controller_parameters()
            self.send_images()

        elif self.model_type == 'model_file':
            # Data file processing
            self.model_file()
            self.compute_controller_params_and_simulations()
            self.send_controller_parameters()
            self.send_images()

        else:
            self.model_undefined()

        self.__del__()

    def model_file (self):
        # Se responde al cliente
        response ="model_accepted"+self.eof
        self.socket.send(response.encode())

        # Receive model data
        self.step_response = self.receive_plain_text()
        #print(self.step_response)

    def model_fotf (self):
        # Se responde al cliente
        response ="model_accepted"+self.eof
        self.socket.send(response.encode('utf-8'))

        # Receive model data
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
        # Send tunning results
        ## Ejecutar el subprocess
        if self.model_type == 'model_fotf':
            command = '../../bash/compute_request.sh '+self.model_str
        elif self.model_type == 'model_file':
            command = '../../bash/compute_request.sh << EOF\n'+self.step_response+'\nEOF\n'
        else:
            pass

        tunning_process = subproc(command,
                                  stdout=PIPE,
                                  shell=True)
        out, err = tunning_process.communicate()
        tunning_process.terminate()
        self.cach_path = out.decode().split('\n')[0]
        print(self.cach_path)

    def send_controller_parameters (self):
        ## Open results file
        file_path = self.cach_path+"/results_table.txt"
        results_file = open(file_path)
        results_file = ''.join(results_file.readlines())

        ## Send file content
        result = results_file+self.eof
        self.socket.send(result.encode('utf-8'))
        print(result)

    def send_images (self):
        ## Send images
        command = '../../bash/wait_and_list_images.sh '+self.cach_path
        tunning_process = subproc(command,
                                  stdout=PIPE,
                                  shell=True)
        out, err = tunning_process.communicate()
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

            print("Recibiendo la confirmación del usuario")
            print(self.socket.recv(512).decode())

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
