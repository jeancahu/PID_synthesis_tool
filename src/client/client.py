#!/usr/bin/env python

import socket
from sys import exit

# import os
# import time
# import getpass

## Global Vars
server_URL = "192.168.0.4"
server_port = 8494

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Se crea el socket
    try:
        client.connect((server_URL, server_port))
    except:
        print("No fue posible ingresar por el puerto ", server_port, server_URL)
        exit(1)

    client.send("Hola".encode())
    datos = client.recv(1000)
    print(datos.decode())
    client.close()

if __name__ == "__main__":
    main()
