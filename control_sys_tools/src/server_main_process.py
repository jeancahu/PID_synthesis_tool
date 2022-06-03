#!/usr/bin/env python3.7
#
# Servidor encargado de realizar la interfaz de comunicación
# entre el programa cliente del móvil y los diferentes módulos
# que conforman la herramienta del lado del servidor.
#
#

import socket
# import os
# import commands
# import MySQLdb as mdb
import threading
import time
# import getpass

# Comunicacion cliente-servidor:
# Utilizar un proceso por cliente
class Client(threading.Thread):
  """ Cliente conectado al server
  """
  def __init__(self, socket_cliente, datos_cliente):
    threading.Thread.__init__(self)
    self.socket = socket_cliente
    self.datos_str = datos_cliente[0] + ":" + str(datos_cliente[1]) # Datos del cliente
    print("El cliente " + self.datos_str + " se ha conectado")

  def run(self):

    #Ahora que se han comunicado es momento de recibir datos:
    """ Cuando se quiera hacer que el cliente se mantenga conectado y el server pueda escuchar varios comandos
    entonces se usara un while y se anulara el del al final.
    """
    while True:
      datos = self.socket.recv(1024) # Recibe 1024 bytes del cliente
      datos.decode('utf-8') # Descodificar datos segun el protocolo

      print("Los datos son: ", datos) # Imprime los datos 
      datos = datos.replace('\n', '')

      #
      # TODO: agregar la lógica para la operación de los datos recibidos del cliente
      # y el cierre de conexión

      self.socket.send("Comando aceptado")
          
  
  def __del__(self):
    
    self.socket.close() # El cliente se despide
    
    
def main(): 
  
  #iniciando.setio()
  server = socket.socket() #Crear socket server  
  server_ip = "1.2.3.4" # TODO: Definir IP o URL en su defecto
  server_default_port = 8494 # Puerto por defecto  


  server.bind((server_ip,
               server_default_port))
  print("Se ha iniciado el server con el puerto" , server_default_port , "como receptor")
  server.listen(1) 
  clients = [] # Lista de clientes

  while True:
    
    try:
      
      socket_cliente, datos_cliente = server.accept()    
      
    except KeyboardInterrupt:

      server.close()
      funciones.clean()
      break
    
    hilo_cliente = Client(socket_cliente, datos_cliente)
    hilo_cliente.start()
    clients.append(hilo_cliente) #Ingresa el cliente en la lista  
    
if __name__ == "__main__": 
  main() 

