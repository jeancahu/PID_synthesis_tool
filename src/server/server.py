#!/usr/bin/env python 

from sys import exit
from sys import argv
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
