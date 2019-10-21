#!/usr/bin/env python3

import socket, re
import cgi

## Global Vars
server_URL = "163.178.124.156"
server_port = 8494
images_path = '../html/images/'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Se crea el socket
try:
    client.connect((server_URL, server_port))
except:
    # print("No fue posible ingresar por el puerto ", server_port, server_URL)
    pass

client.send("model_fotf".encode())
response = client.recv(512)
# print(response.decode())

# Receive model params
# in_model = input("Insert model type (model_fotf/model_file): ")

in_frac_order = str(cgi.FieldStorage()["v"].value)
in_time_const = str(cgi.FieldStorage()["T"].value)
in_prop_const = str(cgi.FieldStorage()["K"].value)
in_dtime_const = str(cgi.FieldStorage()["L"].value)

# Send models parameters
parameters = in_frac_order+","+in_time_const+","+\
    in_prop_const+","+in_dtime_const+"\nEOF"
client.send(parameters.encode())
controller_params = client.recv(2048).decode()
# print(controller_params)

# Receive the first name
image_name = client.recv(512).decode('utf-8')
image_name = image_name.replace('\n','')

images_list = []
while True:
    # print(image_name)
    if "END" in image_name:
        break

    images_list.append(image_name)
    
    # print("ImageNameReceived")
    confirmation="ImageNameReceived".encode('utf-8')
    client.send(confirmation)

    data_bytes = bytes()
    with open(images_path + image_name+".png", 'wb') as f:
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
        
print("Content-type:text/html\r\n\r\n")
print('<html>')
print('<head>')
print('<title>PI/PID Tunning CGI tool web interface</title>')
print('</head>')
print('<body>')
print('<h2>Tunning parameters:</h2>')

print("Fractional parameter is: ", cgi.FieldStorage()["v"].value, '<br>')
print("Time constant is: ", cgi.FieldStorage()["T"].value, '<br>')
print("Proportional constant is: ", cgi.FieldStorage()["K"].value, '<br>')
print("Dead time constant is: ", cgi.FieldStorage()["L"].value, '<br>')

print('<h2>Controller parameters:</h2>')
print(controller_params.replace('\n', "<br>\n"))

print('<h2>Images:</h2>')

for image in images_list:
    print('<img src="/images/'+image+'.png" alt="image">')

print('</body>')
print('</html>')
