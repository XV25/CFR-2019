import sys     # pour la gestion des parametres
import serial  # bibliotheque permettant la communication serie
import time
import numpy as np
from rplidar import RPLidar
import caplidenface as capV
import caplidv5 as capJ
from scipy import signal
from detect_threading_opti import *
import RPi.GPIO as gp


class terminatom():
    """
    cette classe permet de regrouper toutes les fonctions utilisable par la rasp pour commander les differentes
    composant. Les communication necessaire pour chaque action seront ecrite dans ces fonctions.
    """

    def __init__(self, pos_x=0, pos_y=0, angle = 0):
        self.ser = serial.Serial('/dev/ttyACM0',9600, timeout = 1)  #connection serie avec la carte arduino base roulante
        self.ser2 = serial.Serial('/dev/ttyACM1',9600, timeout = 1)
        self.ser3 = serial.Serial('/dev/ttyACM2',9600, timeout = 1)
        self.vg =0
        self.vd = 0
        self.x = pos_x
        self.y = pos_y
        self.theta = angle
        capJ.connect()
        self.vs = PiVideoStream().start()

        res = ''
        while res == '':
            self.ser.write('i')
            res = self.ser.readline()
            print("echec1")
        while res != '':
            res = self.ser.readline()
        print(" 1 : ",res)

        
        res = ''
        while res == '':
            self.ser2.write('i')
            res = self.ser2.readline()
            print("echec2")
        while res != '':
            res = self.ser2.readline()
        print(" 2 : ",res)
        
        res = ''
        while res == '':
            self.ser3.write('i')
            res = self.ser3.readline()
            print("echec3")
        while res != '':
            res = self.ser3.readline()
        print(" 3 : ",res)

        print("Robot pret")
        gp.setmode(gp.BOARD)
        gp.setup(40, gp.IN,pull_up_down=gp.PUD_DOWN)
        gp.setup(38,gp.IN)
        ready = 0
        while ready == 0:
            ready = gp.input(40)

        self.couleur =gp.input(38) # 0 : violet, 1 : jaune
        print("go")
        print("couleur",self.couleur)

        
    '''
    def __del__(self):
        cap.disconnect()
        self.vs.stop()
    '''   
    def __str__(self):
        return "Position : "+str(self.x)+" "+str(self.y)+" "+str(self.theta)
        
        
    #rajouter les variable d'etat utile au fire et a mesure
    def nouvellePos(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y


    
    def Motor(self,vg,vd):
        print(" moteur : ",vg," et ",vd)
        self.vg = vg
        self.vd  = vd
        
        if vg >= 0:
            ldir = chr(0)
        else :
            ldir = chr(1)
                
        self.ser2.write('m')
        self.ser2.readline()
        self.ser2.write(ldir)
        self.ser2.readline()
        pwmL = [abs(vg)//250,abs(vg)%250]
        for i in range (pwmL[0]):
            self.ser2.write(chr(250))
            self.ser2.readline()
        
        
        if vd >= 0:
            ldir = chr(0)
        else :
            ldir = chr(1)
        self.ser.write('m')
        self.ser.readline()
        self.ser.write(ldir)
        self.ser.readline()
        pwm = [abs(vd)//250,abs(vd)%250]
        for i in range (pwm[0]):
            self.ser.write(chr(250))
            self.ser.readline()
        self.ser.write(chr(pwm[1]))
        self.ser.readline()

        self.ser2.write(chr(pwmL[1]))
        self.ser2.readline()
        
        if pwm[1] != 0:
            self.ser.write(chr(0))
            self.ser.readline()

        if pwmL[1] != 0:
            self.ser2.write(chr(0))
            self.ser2.readline()

        self.ser.readline()
        self.ser2.readline()
        
        

    def arret(self):
        while (abs(self.vd) > 20 ) and  ( abs(self.vg) > 20):
            self.Motor(int(self.vg//1.3),int(self.vd//1.3))
        self.Motor(0,0)

    def odometer(self):
        print(" fonction odometre")
        self.ser.write('o')
        #print(self.ser.readline())
        self.ser.readline()
        odoright = int(self.ser.readline())
        self.ser2.write('o')
        self.ser2.readline()
        odoleft = int(self.ser2.readline())
        print(odoleft, odoright)
        return (odoleft,odoright)




    def ultrason(self,mode = 'n'):
        print("ultrason")
        if mode == 'f':
            self.ser3.write('f')
            print(self.ser3.readline())
            u1 = int(self.ser3.readline())
            u2 = int(self.ser3.readline())
        elif mode == 'b':
            self.ser3.write('b')
            print(self.ser3.readline())
            u1 = int(self.ser3.readline())
            u2 = int(self.ser3.readline())
        elif mode == 'l':
            self.ser3.write('l')
            print(self.ser3.readline())
            u1 = int(self.ser3.readline())
            u2 = int(self.ser3.readline())
        elif mode == 'r':
            self.ser3.write('r')
            print(self.ser3.readline())
            u1 = int(self.ser3.readline())
            u2 = int(self.ser3.readline())
        elif mode == 'o':
            self.ser3.write('o')
            print(self.ser3.readline())
            u1 = int(self.ser3.readline())
            u2 = int(self.ser3.readline())
        elif mode == 'p':
            self.ser3.write('p')
            print(self.ser3.readline())
            u1 = int(self.ser3.readline())
            u2 = int(self.ser3.readline())
        else:
            u1 = float('nan')
            u2 = float('nan')
            print(" erreur parametre, f : front, b : back, l : left, r : right")
        return (u1,u2)




    def lidar(self):
        if self.couleur == 0:
            res = capV.main(self.x,self.y,np.pi*signal.sawtooth(self.theta-np.pi/2+np.pi))
        else:
            res = capJ.main(self.x,self.y,np.pi*signal.sawtooth(self.theta-np.pi/2+np.pi))
        #res0 = res[0] + 10 * np.cos(res[2]-np.pi)
        res1 = res[1] + 10 * np.sin(res[2]-np.pi)
        return res[0],res1,res[2]
        
    def majLidar(self):
        lid = self.lidar()
        self.x = lid[0][0]
        self.y = lid[1][0]
        self.theta = lid[2][0]
        print(self)
    
        

    def gold(self):
        print("goldonium")
        self.ser2.write('g')
        print(self.ser2.readline())
        res = ''
        test = ''
        while test != 'f':
            res = self.ser2.readline()
            if len(res) > 0:
                test = res[0]        
        print("fin catch")

    def palet(self):
        print("palet")
        self.ser2.write('p')
        print(self.ser2.readline())
        res = ''
        test = ''
        while test != 'f':
            res = self.ser2.readline()
            if len(res) > 0:
                test = res[0]        
        print("fin catch")


    def drop(self):
        print("balance")
        self.ser2.write('b')
        print(self.ser2.readline())
        res = ''
        test = ''
        while test != 'f':
            res = self.ser2.readline()
            if len(res) > 0:
                test = res[0]        
        print("fin drop")


    def sortirPince(self):
        print("Sortie pince")
        self.ser2.write('c')
        print(self.ser2.readline())
        res = ''
        test = ''
        while test != 'f':
            res = self.ser2.readline()
            if len(res) > 0:
                test = res[0]
        print("fin sortie")

    def sortirPinceBouton(self):
        print("Sortie pince")
        self.ser2.write('e')
        print(self.ser2.readline())
        res = ''
        test = ''
        while test != 'f':
            res = self.ser2.readline()
            if len(res) > 0:
                test = res[0]
        print("fin sortie")

    def rentrerPince(self):
        print("Rentrer pince")
        self.ser2.write('d')
        print(self.ser2.readline())
        res = ''
        test = ''
        while test != 'f':
            res = self.ser2.readline()
            if len(res) > 0:
                test = res[0]


        print("fin Pince rentrer")

    
    def positionGold(self):
        L = detect_gold(self.vs,0,0,4)[1]
        while L == 0:
            L = detect_gold(self.vs,0,0,4)[1]
            print("noPalet")
        print("L",L)
        return L

    def positionPalet(self):
        L = detect_color(self.vs,0,0,4)[1]
        print("L",L)
        return L

    

if __name__ == "__main__":
    rob = terminatom()
    '''
    rob.odometer()
    rob.Motor(400,400)
    time.sleep(5)
    rob.Motor(0,0)
    rob.odometer()
    '''
    
    print(rob.ultrason('f'))
    print(rob.ultrason('r'))
    print(rob.ultrason('l'))
    print(rob.ultrason('b'))
    print(rob.ultrason('o'))
    '''
    rob.positionGold()
    
    rob.sortirPince()
    time.sleep(5)
    rob.rentrerPince()
    
    rob.odometer()

    rob.x = 1325
    rob.y = 755
    rob.theta =np.pi/2
    print(rob.lidar())
    
    rob.positionGold()
    
    rob.gold()
    
    '''
    
    #capJ.disconnect()
    rob.vs.stop()
