#!/usr/bin/env python

import socket as _socket
from pidtuning._internal.client_thread import PID_Client as _PID_client

class Server():
  def __init__(self, address="127.0.0.1", port=10010):
    self.server_address=address
    self.server_port=port

  def run(self):
    """
    Create server socket, listen to request one by one and open
    a thread for every client who connects to the port
    """
    server = _socket.socket(
      _socket.AF_INET, _socket.SOCK_STREAM) # Server socker

    try:
      server.bind((self.server_address, self.server_port))
      print("Server is started at port" , self.server_port)
    except:
      print("Sever failed when it has been trying to start at port",
            self.server_port,
            "it might have been busy")
      return 1

    server.listen(1) # Listen to one request at time
    clients = []     # Clients list

    while True:      # Server keeps waiting for request
      try:
        client_socket, client_data = server.accept()

      except KeyboardInterrupt:
        for csocket in clients:
          csocket.join() # It closes every connection
        server.close()   # It ends the server rutine
        return 0

      client_thread = _PID_Client(client_socket, client_data)
      client_thread.start()         # Start client's thread
      clients.append(client_thread) # It ingress client to the list
