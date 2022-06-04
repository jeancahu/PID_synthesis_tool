#!/usr/bin/env python

from sys import exit
from sys import argv

from subprocess import Popen as subproc
from subprocess import PIPE

# from common.client_thread import Client # FIXME

import socket

## Init
if len(argv) < 3:
  print("Bad args")
  exit(2)

## Global Vars:
server_URL  = str(argv[1])
server_port = int(argv[2])

def main():
  """
  Create server socket, listen to request one by one and open
  a thread for every client who connects to the port
  """
  server = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM) # Server socker
  try:
    server.bind((server_URL, server_port))
    print("Server is started at port" , server_port)
  except:
    print("Sever failed when it has been trying to start at port",
          server_port,
          "it might have been busy")
    exit(1)

  server.listen(1) # Listen to one request at time
  clients = []     # Clients list

  while True:      # Server keeps waiting for request
    try:
      client_socket, client_data = server.accept()

    except KeyboardInterrupt:
      for csocket in clients:
        csocket.join() # It closes every connection
      server.close()   # It ends the server rutine
      exit(0)

    client_thread = Client(client_socket, client_data)
    client_thread.start()         # Start client's thread
    clients.append(client_thread) # It ingress client to the list

if __name__ == "__main__":
  main()
