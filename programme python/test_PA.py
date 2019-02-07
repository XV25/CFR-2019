import serial
import time


port_moteur = '/dev/ttyACM0' #2 

ser_moteur = serial.Serial(port= port_moteur,baudrate=9600 )

time.sleep(2)
ser_moteur.write('f'.encode("utf-8"))
time.sleep(5)
ser_moteur.write('w'.encode("utf-8"))
