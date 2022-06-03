#!/usr/bin/env python

from sys import exit
from sys import argv
import socket, re

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

    client.send("model_fotf".encode())
    response = client.recv(512)
    print(response.decode())

    # Receive model params
    in_model = input("Insert model type (model_fotf/model_file): ")
    in_frac_order = input("Insert fractional order: ")
    in_time_const = input("Insert time constant: ")
    in_prop_const = input("Insert proportional constant: ")
    in_dtime_const = input("Insert dead time constant: ")
    
    # Send models parameters
    parameters = in_frac_order+","+in_time_const+","+\
        in_prop_const+","+in_dtime_const+"\nEOF"
    client.send(parameters.encode())
    controller_params = client.recv(2048)
    print(controller_params.decode())

    # Receive the first name
    image_name = client.recv(512).decode('utf-8')
    image_name = image_name.replace('\n','')
    while True:
        print(image_name)
        if "END" in image_name:
            break

        print("ImageNameReceived")
        confirmation="ImageNameReceived".encode('utf-8')
        client.send(confirmation)

        data_bytes = bytes()
        with open(image_name+".png", 'wb') as f:
            while True:
                data_bytes = b''.join([data_bytes, client.recv(4096)])
                end_line = data_bytes[-20:].decode('utf-8', errors="ignore")

                # Search for PNG end format sequence
                if 'IENDB`' in end_line and \
                   ( "RD\n" in end_line[-3:] or "END" in end_line[-3:]):
                    image_name = re.sub('.*IENDB`','', end_line)
                    image_name = image_name.replace('\n','')
                    break
            f.write(data_bytes)
            del(data_bytes)
            f.close()

if __name__ == "__main__":
    main()
    exit(0)
