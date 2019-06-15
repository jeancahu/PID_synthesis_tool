#!/usr/bin/env python 

import socket
# import os
# import commands
# import MySQLdb as mdb
import threading
import time
# import getpass

import time # necesario para los delays


## Global Vars:
#server_URL = "carara.eie.ucr.ac.cr"
server_URL = "192.168.0.4"
server_port = 8494

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
    COMMENTARIO
    """

    datos = self.socket.recv(1024) # Recibe 1024 bytes del cliente
    datos = datos.decode('utf-8') # Decodificar datos según el protocolo
    datos = datos.replace('\n', '')
    print("Los datos son: ", datos) # Imprime los datos en la bitácora

    self.socket.send("Comando acceptado".encode('utf-8')) # Se responde al cliente

  def __del__(self):
    self.socket.close() # El cliente se despide


def main(): 

  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crear socket server  
  server.bind((server_URL, server_port))
  print("Se ha iniciado el server con el puerto" , server_port , "como receptor")
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
