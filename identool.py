#!/bin/python2
# Escrito por, Jeancarlo Hidalgo
# Este script recibe del stin la direccion de un fichero.csv con la fila 0
# respuesta al escalon unitario del sistema, fila 1, arreglo de tiempo.

import csv
import sys
import numpy as np

planta=[]

def alfaro123c(K):
    nombre="alfaro123c"
    a=0.910
    b=1.262
    contador=0
    for i in planta[0]:
        if abs(i) < abs(0.25*K):
            tiempo1=planta[1][contador]
        if abs(i) < abs(0.75*K):
            tiempo2=planta[1][contador]
        contador=contador+1
    T=a*(tiempo2-tiempo1)
    L=b*tiempo1+(1-b)*tiempo2
    print "El primer tiempo en el caso de",nombre,"es",tiempo1
    print "El segundo tiempo en el caso de",nombre,"es",tiempo2
    print "Por tanto, con un a de",a,"y un b de",b,"se tiene:"
    print " "
    print "   ",K,"e^(-",L,"s)"
    print "   ----------------------"
    print "     ",T,"s + 1"
    print " "
    
def broida(K):
    nombre="broida"
    a=5.500
    b=2.800
    contador=0
    for i in planta[0]:
        if abs(i) < abs(0.28*K):
            tiempo1=planta[1][contador]
        if abs(i) < abs(0.40*K):
            tiempo2=planta[1][contador]
        contador=contador+1
    T=a*(tiempo2-tiempo1)
    L=b*tiempo1+(1-b)*tiempo2
    print "El primer tiempo en el caso de",nombre,"es",tiempo1
    print "El segundo tiempo en el caso de",nombre,"es",tiempo2
    print "Por tanto, con un a de",a,"y un b de",b,"se tiene:"
    print " "
    print "   ",K,"e^(-",L,"s)"
    print "   ----------------------"
    print "     ",T,"s + 1"
    print " "
    
def ho_et_al(K):
    nombre="ho_et_al"
    a=0.670
    b=1.290
    contador=0
    for i in planta[0]:
        if abs(i) < abs(0.35*K):
            tiempo1=planta[1][contador]
        if abs(i) < abs(0.85*K):
            tiempo2=planta[1][contador]
        contador=contador+1
    T=a*(tiempo2-tiempo1)
    L=b*tiempo1+(1-b)*tiempo2
    print "El primer tiempo en el caso de",nombre,"es",tiempo1
    print "El segundo tiempo en el caso de",nombre,"es",tiempo2
    print "Por tanto, con un a de",a,"y un b de",b,"se tiene:"
    print " "
    print "   ",K,"e^(-",L,"s)"
    print "   ----------------------"
    print "     ",T,"s + 1"
    print " "
    
def chen_y_yang(K):
    nombre="chen_y_yang"
    a=1.400
    b=1.540
    contador=0
    for i in planta[0]:
        if abs(i) < abs(0.33*K):
            tiempo1=planta[1][contador]
        if abs(i) < abs(0.67*K):
            tiempo2=planta[1][contador]
        contador=contador+1
    T=a*(tiempo2-tiempo1)
    L=b*tiempo1+(1-b)*tiempo2
    print "El primer tiempo en el caso de",nombre,"es",tiempo1
    print "El segundo tiempo en el caso de",nombre,"es",tiempo2
    print "Por tanto, con un a de",a,"y un b de",b,"se tiene:"
    print " "
    print "   ",K,"e^(-",L,"s)"
    print "   ----------------------"
    print "     ",T,"s + 1"
    print " "
    
def smith(K):
    nombre="smith"
    a=1.500
    b=1.500
    contador=0
    for i in planta[0]:
        if abs(i) < abs(0.28*K):
            tiempo1=planta[1][contador]
        if abs(i) < abs(0.63*K):
            tiempo2=planta[1][contador]
        contador=contador+1
    T=a*(tiempo2-tiempo1)
    L=b*tiempo1+(1-b)*tiempo2
    print "El primer tiempo en el caso de",nombre,"es",tiempo1
    print "El segundo tiempo en el caso de",nombre,"es",tiempo2
    print "Por tanto, con un a de",a,"y un b de",b,"se tiene:"
    print " "
    print "   ",K,"e^(-",L,"s)"
    print "   ----------------------"
    print "     ",T,"s + 1"
    print " "
    
def viteckova_et_al(K):
    nombre="viteckova_et_al"
    a=1.245
    b=1.498
    contador=0
    for i in planta[0]:
        if abs(i) < abs(0.33*K):
            tiempo1=planta[1][contador]
        if abs(i) < abs(0.70*K):
            tiempo2=planta[1][contador]
        contador=contador+1
    T=a*(tiempo2-tiempo1)
    L=b*tiempo1+(1-b)*tiempo2
    print "El primer tiempo en el caso de",nombre,"es",tiempo1
    print "El segundo tiempo en el caso de",nombre,"es",tiempo2
    print "Por tanto, con un a de",a,"y un b de",b,"se tiene:"
    print " "
    print "   ",K,"e^(-",L,"s)"
    print "   ----------------------"
    print "     ",T,"s + 1"
    print " "

def viteckova_et_al_PDMTM(K):
    nombre="viteckova_et_al"
    a=0.794
    b=1.937
    contador=0
    for i in planta[0]:
        if abs(i) < abs(0.33*K):
            tiempo1=planta[1][contador]
        if abs(i) < abs(0.70*K):
            tiempo2=planta[1][contador]
        contador=contador+1
    T=a*(tiempo2-tiempo1)
    L=b*tiempo1+(1-b)*tiempo2
    print "El primer tiempo en el caso de",nombre,"es",tiempo1
    print "El segundo tiempo en el caso de",nombre,"es",tiempo2
    print "Por tanto, con un a de",a,"y un b de",b,"se tiene:"
    print " "
    print "   ",K,"e^(-",L,"s)"
    print "   ----------------------"
    print "     (",T,"s + 1 )^2"
    print " "

def ho_et_al_PDMTM(K):
    nombre="ho_et_al"
    a=0.463
    b=1.574
    contador=0
    for i in planta[0]:
        if abs(i) < abs(0.35*K):
            tiempo1=planta[1][contador]
        if abs(i) < abs(0.85*K):
            tiempo2=planta[1][contador]
        contador=contador+1
    T=a*(tiempo2-tiempo1)
    L=b*tiempo1+(1-b)*tiempo2
    print "El primer tiempo en el caso de",nombre,"es",tiempo1
    print "El segundo tiempo en el caso de",nombre,"es",tiempo2
    print "Por tanto, con un a de",a,"y un b de",b,"se tiene:"
    print " "
    print "   ",K,"e^(-",L,"s)"
    print "   ----------------------"
    print "     (",T,"s + 1 )^2"
    print " "

def alfaro123c_PDMTM(K):
    nombre="alfaro123c"
    a=0.578
    b=1.555
    contador=0
    for i in planta[0]:
        if abs(i) < abs(0.25*K):
            tiempo1=planta[1][contador]
        if abs(i) < abs(0.75*K):
            tiempo2=planta[1][contador]
        contador=contador+1
    T=a*(tiempo2-tiempo1)
    L=b*tiempo1+(1-b)*tiempo2
    print "El primer tiempo en el caso de",nombre,"es",tiempo1
    print "El segundo tiempo en el caso de",nombre,"es",tiempo2
    print "Por tanto, con un a de",a,"y un b de",b,"se tiene:"
    print " "
    print "   ",K,"e^(-",L,"s)"
    print "   ----------------------"
    print "     (",T,"s + 1 )^2"
    print " "

def alfaro123c_SOMTM(K):
    nombre="alfaro123c"
    contador=0
    for i in planta[0]:
        if abs(i) < abs(0.25*K):
            tiempo1=planta[1][contador]
        if abs(i) < abs(0.50*K):
            tiempo2=planta[1][contador]
        if abs(i) < abs(0.75*K):
            tiempo3=planta[1][contador]
        contador=contador+1

    a_num=1.0*(-0.6240*tiempo1 + 0.9866*tiempo2 -0.3626*tiempo3)
    a_den=1.0*(0.3533*tiempo1 -0.7036*tiempo2 +0.3503*tiempo3)
    a=a_num/a_den

    if a > 1 or a < 0:
        print "No es posible utilizar el criterio de",nombre,"en este sistema"
        print "Se obtuvo un t25:",tiempo1,"y un t75:",tiempo3
        print " "
        return 1
    
    T1_num=1.0*(tiempo3 - tiempo1)
    T1_den=1.0*(0.9866+0.8036*a)
    T1=T1_num/T1_den
    T2=a*T1
    L=tiempo3 - (1.3421+1.3455*a)*T1
        
    print "El primer tiempo en el caso de",nombre,"es",tiempo1
    print "El segundo tiempo en el caso de",nombre,"es",tiempo2
    print "El tercer tiempo en el caso de",nombre,"es",tiempo3
    print "Se obtiene un a de ",a,", el modelo es el siguiente:"
    print " "
    print "            ",K,"e^(-",L,"s)"
    print "   --------------------------------------------------"
    print "     (",T1,"s + 1 )(",T2,"s + 1 )"
    print " "
    return 0

def stark_SOMTM(K):
    nombre="stark"
    contador=0
    for i in planta[0]:
        if abs(i) < abs(0.15*K):
            tiempo1=planta[1][contador]
        if abs(i) < abs(0.45*K):
            tiempo2=planta[1][contador]
        if abs(i) < abs(0.75*K):
            tiempo3=planta[1][contador]
        contador=contador+1

    x_num=(tiempo2-tiempo1)*1.0
    x_den=(tiempo3-tiempo1)*1.0
    x=x_num/x_den
    Xi=(1.0*(0.0805 -5.547*(0.475-x)*(0.475-x)))/(1.0*(x-0.356))
    

    if Xi > 1: # Sobre amortiguado

        funXi= 2.6*Xi -0.6
        funXi_L=0.922*(np.power(1.66,Xi))
        wn=(funXi*1.0)/(1.0*(tiempo3-tiempo1))

        L=tiempo2-(funXi_L*1.0)/(wn*1.0)
        T1=Xi+np.sqrt(Xi*Xi -1)
        T1=(1.0*T1)/wn
        T2=Xi-np.sqrt(Xi*Xi -1)
        T2=(1.0*T2)/wn
        
        print "El primer tiempo en el caso de",nombre,"es",tiempo1
        print "El segundo tiempo en el caso de",nombre,"es",tiempo2
        print "El tercer tiempo en el caso de",nombre,"es",tiempo3
        print " "
        print "            ",K,"e^(-",L,"s)"
        print "   --------------------------------------------------"
        print "     (",T1,"s + 1 )(",T2,"s + 1 )"
        print " "
        return 0
        
    elif Xi < 1 or Xi == 1:

        funXi=0.708*(np.power(2.811,Xi))
        funXi_L=0.922*(np.power(1.66,Xi))
        wn=(funXi*1.0)/(1.0*(tiempo3-tiempo1))

        L=tiempo2-(funXi_L*1.0)/(wn*1.0)
        
        print "El primer tiempo en el caso de",nombre,"es",tiempo1
        print "El segundo tiempo en el caso de",nombre,"es",tiempo2
        print "El tercer tiempo en el caso de",nombre,"es",tiempo3        
        print " "
        print "            ",K,"e^(-",L,"s)"
        print "   --------------------------------------------------"
        print "     ( s^2 +",2.0*Xi*wn,"s +",wn*wn,")"
        print " "
        return 0

    else:
        print "No se pudo ejecutar el criterio",nombre
        return 1
    
    
def main():
    
    tablefile=open(sys.argv[1], "rb")
    reader=csv.reader(tablefile)
    for row in reader:
        result=map(float, row) # Convertir todo a float
        planta.append(result)

    print "*** Programa de identificacion de modelo de primer orden mas tiempo muerto"
    print "*** Modelos de primer orden mas tiempo muerto:"
    print " "
    K=planta[0][-1] # Ganancia
    alfaro123c(K)
    broida(K)
    ho_et_al(K)
    chen_y_yang(K)
    smith(K)
    viteckova_et_al(K)

    print "*** Modelos de polo doble mas tiempo muerto:"
    print " "
    alfaro123c_PDMTM(K)
    ho_et_al_PDMTM(K)
    viteckova_et_al_PDMTM(K)

    print "*** Modelos de segundo orden mas tiempo muerto:"
    print " "
    alfaro123c_SOMTM(K)
    stark_SOMTM(K)
    
main()

