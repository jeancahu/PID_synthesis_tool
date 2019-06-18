#!/usr/bin/env python

from sys import exit
from sys import argv
import socket

## Init
if len(argv) < 3:
    print("Insuficientes argumentos")
    exit(2)     

## Global Vars
server_URL = str(argv[1])
server_port = int(argv[2])

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Se crea el socket
    try:
        client.connect((server_URL, server_port))
    except:
        print("No fue posible ingresar por el puerto ", server_port, server_URL)
        exit(1)

    client.send("model".encode())
    datos = client.recv(1000)
    print(datos.decode())
    client.send("1.5,4,4,4,1.4,PID".encode())
    datos = client.recv(1000)
    print(datos.decode())

    
    
    #client.send("response_file".encode())
    #client.send("test".encode())

    ## Se reciben los parámetros
    datos = client.recv(1000)
    print(datos.decode())
    client.close()

if __name__ == "__main__":
    main()
    exit(0)
