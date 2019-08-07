#!/usr/bin/env python

import threading
import socket
import base64
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
        # Datos del cliente
        self.datos_str = datos_cliente[0] + ":" + str(datos_cliente[1])
        self.sha_id = ''
        self.eof = '\n'+"EOF"+'\n'
        print("El cliente " + self.datos_str + " se ha conectado")
    
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
        model = model.decode()[:10] # Decodificar datos según el protocolo
        print("El modelo es de tipo: ", model) # Imprime los datos en la bitácora
  
        if model == 'model_fotf':
            self.model_fotf()
        elif model == 'model_file':
            self.model_file()
        else:
            self.model_undefined()

        self.__del__()
        
    def model_file (self):
        # Se responde al cliente
        response ="model_accepted"+self.eof
        self.socket.send(response.encode())

        # Receive model data
        #print(self.receive_plain_text())
        step_response = self.receive_plain_text()
        #print(step_response)
        command = '../../bash/compute_request.sh << EOF\n'+step_response+'\nEOF\n'
        tunning_process = subproc(command,
                                  stdout=PIPE,
                                  shell=True)
        out, err = tunning_process.communicate()
        print(out.decode())

    def model_fotf (self):
        # Se responde al cliente
        response ="model_accepted"+self.eof
        self.socket.send(response.encode('utf-8'))
        
        # Receive model data
        data = self.socket.recv(512).decode()
        data = data.replace("\nEOF\n",'')
        data = data.replace('\n',' ')
        print(data)
        
        # Send tunning results
        ## Ejecutar el subprocess
        command = '../../bash/compute_request.sh '+data.replace(',',' ')
        tunning_process = subproc(command,
                                  stdout=PIPE,
                                  shell=True)
        out, err = tunning_process.communicate()

        ## Open results file
        cach_path = out.decode().split('\n')[0]
        file_path = cach_path+"/results_table.txt"
        results_file = open(file_path)
        results_file = ''.join(results_file.readlines())

        ## Send file content
        result = results_file+self.eof
        tunning_process.terminate()
        print(result)
        self.socket.send(result.encode('utf-8'))

        ## Send images
        command = '../../bash/wait_and_list_images.sh '+cach_path
        tunning_process = subproc(command,
                                  stdout=PIPE,
                                  shell=True)
        out, err = tunning_process.communicate()
        images_str = out.decode()
        images_list = images_str.split(',')
        print(images_list)

        ####
        with open(cach_path+'/'+images_list[1], "rb") as imageFile:
            #image = base64.b64encode(imageFile.read())
            image = imageFile.read()
            #print(image)

            #size_bytes = str(len(image)) + '\n'
            #self.socket.send(size_bytes.encode('utf-8'))
            self.socket.sendall(image)
        ####
        
    def model_undefined (self):
        # Se responde al cliente
        response ="model_denied"+self.eof
        self.socket.send(response.encode())

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
