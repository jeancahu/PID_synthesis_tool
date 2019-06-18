#!/usr/bin/env python 

from sys import exit
from sys import argv
from subprocess import Popen as subproc
from subprocess import PIPE
import socket
import threading
import time

## Init
if len(argv) < 3:
  print("Insuficientes argumentos")
  exit(2)

## Global Vars:
server_URL = str(argv[1])
server_port = int(argv[2])


# Comunicacion cliente-servidor:
class Client(threading.Thread):
  """ Cliente conectado al server
  """
  def __init__(self, socket_cliente, datos_cliente):
    threading.Thread.__init__(self)
    self.socket = socket_cliente
    self.datos_str = datos_cliente[0] + ":" + str(datos_cliente[1]) # Datos del cliente
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
    datos = self.socket.recv(512) # Recibe 512 bytes del cliente
    datos = datos.decode('utf-8') # Decodificar datos según el protocolo
    datos = datos.replace('\n', '')
    print("Los datos son: ", datos) # Imprime los datos en la bitácora

    if datos == 'model':
      self.socket.send("Comando acceptado".encode('utf-8')) # Se responde al cliente
      datos = self.socket.recv(512) # Recibe 512 bytes del cliente
      datos = datos.decode('utf-8') # Decodificar datos según el protocolo
      datos = datos.replace('\n', '')
      datos = datos.replace(',',' ')
      print("Los parámetros son: ", datos) # Imprime los datos en la bitácora
      self.socket.send("Parámetros recibidos".encode('utf-8')) # Se responde al cliente

      ## Ejecutar el subprocess
      command = '../tunning/tunning.py '+datos
      tunning_process = subproc(command, stdout=PIPE, shell=True)
      out, err = tunning_process.communicate() 
      result = out.decode('utf-8')
      result = result.split('\n')

      response = ""
      #print(result)
      for lin in result:
        if lin.startswith('R:'):
          print(lin)
          response += lin.split('\t')[2]+','
          #print(lin.split('\t')[2])

      response = response[0:-1] # Eliminar la coma final
      response = response.replace(' ','') # Eliminar espacios
      #print(response)
      tunning_process.terminate()

      ## Se envían los parámetros al cliente
      self.socket.send(response.encode('utf-8'))
      
        
    elif datos == 'response_file':
      self.socket.send("Comando acceptado".encode('utf-8')) # Se responde al cliente
    else:
      self.socket.send("Comando desconocido".encode('utf-8')) # Se responde al cliente

    self.__del__() # Destruye la conexión

  def __del__(self):
    print("El cliente " + self.datos_str + " se ha desconectado")
    self.socket.close() # El cliente se despide


def main(): 

  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crear socket server  
  try:
    server.bind((server_URL, server_port))
    print("Se ha iniciado el server con el puerto" , server_port , "como receptor")
  except:
    print("Fue imposible inicializar el server con el puerto", server_port)
    exit(1)

  server.listen(1)
  clients = [] # Lista de clientes

  while True:
    try:
      socket_cliente, datos_cliente = server.accept()

    except KeyboardInterrupt:
      server.close()
      break

    hilo_cliente = Client(socket_cliente, datos_cliente)
    hilo_cliente.start()
    clients.append(hilo_cliente) # Ingresa el cliente en la lista

if __name__ == "__main__": 
  main()
  exit(0)
