
import sys     # pour la gestion des parametres
import serial  # bibliotheque permettant la communication serie
import time
#ser = serial.Serial('/dev/ttyACM0',9600)
ser = serial.Serial('COM7',9600)
f='f'.encode("utf-8")
w="w".encode("utf-8")
o="o".encode("utf-8")
l="l".encode("utf-8")
r='r'.encode("utf-8")
b="b".encode("utf-8")
#Programme chemin à suivre
#fonction de déplacements
def forward(d):#prend en argument la distance en centimétre à parcourir par le robot 
    distance=0
    ser.write(f)
    while float(ser.readline())>1:
        pass
    while distance<d:
        while type(eval(ser.readline()))!= float:
            pass
        distance=float(ser.readline())
    ser.write(w)    
    ser.write(o)
    
def backward(d):
    distance_b=0
    ser.write(b)
    while float(ser.readline())>1:
        pass
    while distance_b<d:
        while type(eval(ser.readline()))!= float:
            pass
        distance_b=float(ser.readline())
    ser.write(w)    
    ser.write(o)

def right(a):#prend l'angle en radians 
    angle_r=0
    ser.write(r)
    while float(ser.readline())>1:
        pass
    while angle_r<a:
        while type(eval(ser.readline()))!= float:
            pass
        angle_r=float(ser.readline())
    ser.write(w)    
    ser.write(o)
    
def left(a):
    angle_l=0
    ser.write(l)
    while float(ser.readline())>1:
        pass
    while angle_l<a:
        while type(eval(ser.readline()))!= float:
            pass
        angle_l=float(ser.readline())
    ser.write(w)    
    ser.write(o)
    
time.sleep(2)
backward(1000)
time.sleep(2)
right(90)
time.sleep(2)
left(90)


ser.close()
