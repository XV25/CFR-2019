# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 08:59:15 2019

@author: Bertrand-predator
"""

import matplotlib.pyplot as plt
import numpy as np
import serial
import time
    

def process(rgb):
    div = 255
    
    l = rgb[:-2].decode("utf-8").split(" ")
    r = min(eval(l[0])/div, 1)
    g = min(eval(l[1])/div, 1)
    b = min(eval(l[2])/div, 1)
    
    ma = max(r ,g, b)
    mi = min(r, g, b)
    
    if(ma == mi):
        t = 0
    elif(ma == r):
        t = (60*(g-b)/(ma-mi)+360)%360
    elif(ma == g):
        t = (60*(b-r)/(ma-mi)+120)
    elif(ma == b):
        t = (60*(r-g)/(ma-mi)+240)
        
    return t

def reconnaissance_couleur(t):
    a,b,c,d,e,f=95,140,180,220,300,350

    if a<t and t<b :
        return('Vert')
    if c<t and t<d :
        return('Rouge')
    if e<t and t<f :
        return('Bleu')
        
        
#port='/dev/ttyUSB1',
# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(

    port='COM4',

    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen()

while 1 :
    ine = ''    
    ine = ser.readline()

    if ine != '':
        t = process(ine)
        print(t,reconnaissance_couleur(t))
        




    
    
