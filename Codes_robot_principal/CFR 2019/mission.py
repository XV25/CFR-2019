import time
import terminatom2 as tm
import matplotlib.pyplot as plt 
import numpy as np
import signal as sig
from scipy import signal
from deplacement import *
from threading import Timer
import caplidv5 as capJ
import sys


def arret():
    rob.Motor(0,0)
    print("fin run")

def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    rob.Motor(0,0)
    
    sys.exit(1)





def missionJaune(rob):
    #-------------------------------------
    #------- mission ---------------------
    #-------------------------------------
    rob.x,rob.y,rob.theta = 450,295,-np.pi
    a = np.array([[450],[295]])
    b = np.array([[270],[295+10]])

    #------Depart--------------------

    x1,y1,theta1 = deplacement(rob,a,b)
    time.sleep(0.5)
    print(rob)
    #---------Pose 1-----------------

    deplacementAngle(rob,-np.pi/2+0.1)
    time.sleep(2)
    rob.theta = -np.pi/2+0.1
    #recalageMurDroit(rob)
    recalageLidar(rob,-np.pi/2+0.1)
    print(rob)
    rob.majLidar()
    print(rob)
    '''
    rob.sortirPinceBouton()
    time.sleep(0.5)
    rob.rentrerPince()
    '''
    #----------Pose 2 ---------------
    a = np.array([[rob.x],[rob.y]])
    b = np.array([[rob.x-100],[1580]])

    x2,y2,theta2 = deplacementArY(rob,a,b,1)
    time.sleep(0.5)
    rob.sortirPince()
    a = np.array([[rob.x],[rob.y]])
    b = np.array([[rob.x+130],[rob.y+60]])
    deplacementArY(rob,a,b,1)
    time.sleep(0.5)
    rob.rentrerPince()
    
    u1 = 150
    u2 = -150
    rob.Motor(int(u1),int(u2))
    time.sleep(0.3)
    rob.Motor(0,0)

    
    rob.x = 310
    rob.y = 1800
    rob.theta= -np.pi/2
    recalageLidar(rob,-np.pi/2)
    time.sleep(0.5)

    #---------Pose 3 ----------------

    rob.theta = -np.pi/2
    a = np.array([[rob.x],[rob.y]])
    b = np.array([[rob.x+40],[2220]])

    x3,y3,theta3 = deplacementArY(rob,a,b,1)
    time.sleep(0.5)
    rob.x = 320
    rob.y = 2270
    rob.theta = -np.pi/2
    recalageLidar(rob,-np.pi/2)

    #rob.lidar()
    print(rob)
    recalageGold(rob)
    time.sleep(0.5)


    rob.gold()

    #------- Pose Goldonium----------


    
    a = np.array([[rob.x],[rob.y]])
    b = np.array([[rob.x+30],[1300]])
    x4,y4,theta4 = deplacementY(rob,a,b,1)
    time.sleep(0.5)
    #--------Pose 4 -----------------

    deplacementAngle(rob,0)
    time.sleep(0.5)
    rob.x = 300
    rob.y = 1320
    rob.theta =0
    recalageLidar(rob,0)
    time.sleep(0.5)
    rob.theta =0

    #rob.majLidar()
    print(rob)

    #--------Pose 5 -----------------
    
    a = np.array([[rob.x],[rob.y]])
    b = np.array([[1100],[rob.y]])
    rob.theta = 0
    x5,y5,theta5 = deplacementX(rob,a,b,1)
    time.sleep(0.5)
    a = np.array([[rob.x],[rob.y]])
    b = np.array([[1280],[rob.y]])
    x5,y5,theta5 = deplacementX(rob,a,b,0)
    rob.x = 1400
    rob.y = 1300
    rob.theta =0
    rob.majLidar()
    print(rob)

    #---------Pose 6 ----------------

    deplacementAngle(rob,np.pi/2-0.2)
    time.sleep(0.5)
    rob.theta = np.pi/2-0.2
    recalageLidar(rob,np.pi/2-0.2)
    time.sleep(0.5)
    rob.majLidar()


    #---------Pose 7 -----------------

    a = np.array([[rob.x],[rob.y]])
    b = np.array([[rob.x+30],[rob.y+100]])
    x4,y4,theta4 = deplacementY(rob,a,b)
    time.sleep(0.5)
    rob.drop()
    
    #----------Pose 8 (balance)----------
    
    
    rob.vs.stop()


def missionViolet(rob):
    
    rob.x,rob.y,rob.theta = 450,2705,-np.pi
    
    a = np.array([[450],[2705]])
    b = np.array([[310],[2705]])
    
    #------Depart--------------------

    x1,y1,theta1 = deplacement(rob,a,b)
    time.sleep(0.5)
    print(rob)
    #---------Pose 1-----------------
    
    deplacementAngle(rob,-np.pi/2+0.05)
    time.sleep(0.5)
    
    rob.theta = -np.pi/2
    rob.y = 2670
    rob.x = 310
    #recalageMurDroit(rob)
    recalageLidar(rob,-np.pi/2)
    print(rob)
    rob.majLidar()
    print(rob)
    '''
    rob.sortirPinceBouton()
    time.sleep(0.5)
    rob.rentrerPince()
    '''
     #----------Pose 2 ---------------

    a = np.array([[rob.x],[rob.y]])
    b = np.array([[rob.x+115],[1430]])

    x2,y2,theta2 = deplacementY(rob,a,b,2)
    time.sleep(0.5)
    #recalageMurDroit(rob)
    #time.sleep(1)
    rob.x = 310
    rob.y = 1420
    recalageLidar(rob,-np.pi/2)
    rob.sortirPince()
    a = np.array([[rob.x],[rob.y]])
    b = np.array([[rob.x+160],[rob.y-100]])
    deplacementY(rob,a,b,2)
    time.sleep(0.5)
    rob.rentrerPince()


    u1 = -150
    u2 = 150
    rob.Motor(int(u1),int(u2))
    time.sleep(0.2)
    rob.Motor(0,0)
    
    rob.x = 310
    rob.y = 1320
    recalageLidar(rob,-np.pi/2)
    time.sleep(0.5)

    #---------Pose 3 ----------------


    rob.theta = -np.pi/2
    a = np.array([[rob.x],[rob.y]])
    b = np.array([[rob.x+100],[840]])

    x3,y3,theta3 = deplacementY(rob,a,b,2)
    time.sleep(0.5)
    rob.x = 320
    rob.y = 780
    rob.theta = -np.pi/2
    recalageLidar(rob,-np.pi/2)

    rob.lidar()
    print(rob)
    recalageGold(rob)
    time.sleep(0.5)


    rob.gold()

    #------- Pose Goldonium----------
    
    a = np.array([[rob.x],[rob.y]])
    b = np.array([[rob.x],[1810]])
    x4,y4,theta4 = deplacementArY(rob,a,b,1)
    time.sleep(0.5)
    
    #--------Pose 4 -----------------

    deplacementAngle(rob,0.05)
    time.sleep(0.5)
    rob.x = 310
    rob.y = 1800
    rob.theta =0
    recalageLidar(rob,0)
    #time.sleep(0.5)
    #rob.theta =0-0.2

    #rob.majLidar()
    print(rob)

    #--------Pose 5 -----------------

    a = np.array([[rob.x],[rob.y]])
    b = np.array([[1050],[rob.y]])
    rob.theta = 0
    x5,y5,theta5 = deplacementX(rob,a,b,1)
    time.sleep(0.5)
    a = np.array([[rob.x],[rob.y]])
    b = np.array([[1280],[rob.y]])
    x5,y5,theta5 = deplacementX(rob,a,b,0)
    time.sleep(0.5)
    rob.x = 1325
    rob.y = 1690
    rob.theta =0
    rob.majLidar()
    print(rob)

    #---------Pose 6 ----------------

    deplacementAngle(rob,np.pi/2+0.2)
    time.sleep(0.5)
    rob.theta = np.pi/2+0.2
    recalageLidar(rob,np.pi/2+0.2)
    time.sleep(0.5)
    rob.majLidar()


    #---------Pose 7 -----------------

    a = np.array([[rob.x],[rob.y]])
    b = np.array([[rob.x+70],[rob.y-100]])
    rob.theta = np.pi/2
    x6,y6,theta6 = deplacementArY(rob,a,b)
    time.sleep(0.5)
    #recalageLidar(rob,np.pi/2)
    #rob.majLidar()

    rob.drop()
    
    rob.vs.stop()

def missionHomol(rob):
    a = np.array([[0],[0]])
    b = np.array([[0],[-300]])
    rob.theta = np.pi/2
    x6,y6,theta6 = deplacementArY(rob,a,b,1)
    print("fin ligne")


if __name__=="__main__":
    #t = Timer(100.0,arret)
    rob = tm.terminatom(450,295,-np.pi)
    sig.signal(sig.SIGALRM, service_shutdown)
    sig.alarm(97)
    #t.start()
    
    if rob.couleur == 0:
        missionViolet(rob)
    else:
        missionJaune(rob)
    
