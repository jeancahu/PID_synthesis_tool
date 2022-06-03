#!/usr/bin/env python 

from sys import exit
from sys import argv
from subprocess import Popen as subproc
from subprocess import PIPE
from common.client_thread import Client
from hashlib import sha224 as sha
import socket
import time

## Init
if len(argv) < 3:
  print("Insuficientes argumentos")
  exit(2)

## Global Vars:
server_URL  = str(argv[1])
server_port = int(argv[2])

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
      for csocket in clients:
        csocket.join()
      server.close()
      exit(0)

    client_thread = Client(socket_cliente, datos_cliente)
    client_thread.start()
    clients.append(client_thread) # Ingresa el cliente en la lista

if __name__ == "__main__": 
  main()
