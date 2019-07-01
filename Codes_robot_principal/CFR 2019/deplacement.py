import time
import terminatom2 as tm
import matplotlib.pyplot as plt 
import numpy as np
from scipy import signal

r = 39
alpha1 = 0.3
alpha2 = 0.3
l = 310
V = 240
dt = 0.05
K = 4
Kar = 4
t= time.time()

distanceSecu = 250

def sign(a):
    if a >= 0:
        return 1
    else:
        return -1


    
def control(x,a,b):
    phi = np.arctan2(b[1,0]-a[1,0],b[0,0]-a[0,0])
    m = x[0:2].reshape((2,1))
    e = np.linalg.det(np.hstack((b-a,m-a)))/np.linalg.norm(b-a)
    thetabar = phi - np.arctan(e)
    angle = K*np.arctan(np.tan(( thetabar -x [2,0] )/2))
    u2 = (angle*l/r*alpha1 + 2*V)* 0.5 
    u1 = 2*V - u2
    return np.array([ [u1],[u2]])



def controlAr(x,a,b):
    x2 = x
    x2[2,0] = np.pi*signal.sawtooth( (x[2,0]-np.pi)+np.pi)
    u1,u2 = control(x2,a,b)

    phi = np.arctan2(b[1,0]-a[1,0],b[0,0]-a[0,0])
    m = x2[0:2].reshape((2,1))
    e = np.linalg.det(np.hstack((b-a,m-a)))/np.linalg.norm(b-a)
    thetabar = phi - np.arctan(e)
    angle = Kar*np.arctan(np.tan(( thetabar -x2[2,0] )/2))
    u2 = (angle*l/r*alpha1 + 2*V)* 0.5 
    u1 = 2*V - u2 
    return np.array([ [-u2-6],[-u1]])





def controlangle(x,angle):
    er = np.pi*signal.sawtooth(angle-x[2,0]+np.pi)
    print('---------------------')
    print(angle, np.pi*signal.sawtooth(x[2,0]+np.pi), er)
    u1 = -sign(er)*120
    u2 = sign(er)*120
    return np.array([ [u1],[u2]])

def maj(rob,encodG,encodD):
    v1 = encodG*r*2*np.pi/(dt*1024)
    v2 = encodD*r*2*np.pi/(dt*1024)
    dx = (v1+v2)*np.cos(rob.theta)/2
    dy = (v1+v2)*np.sin(rob.theta)/2
    dtheta = (v2-v1)/l
    rob.x = rob.x + dt*dx
    rob.y = rob.y + dt*dy
    rob.theta = rob.theta + dt*dtheta
    return rob
    

def drawplateau():
    plt.plot([0,0],[0,3000],'black')
    plt.plot([0,2000],[3000,3000],'black')
    plt.plot([2000,2000],[3000,0],'black')
    plt.plot([2000,0],[0,0],'black')


def detectObstacleAv(rob,u0,mode,t0):
    ob = 0
    t= t0
    if mode >= 1:
        u = u0.copy()
        obstacle = rob.ultrason('o')[0]
        if obstacle <= distanceSecu:# and obstacle !=0:
            print("obstable",obstacle)
            u[0,0],u[1,0] = 0,0
            ob = 1
            print(t0)
            if time.time() -t0 >= 5:
                u[0,0],u[1,0] = -120,-120
        ult = rob.ultrason('f')
        if mode == 2:
            obstacle = ult[1]
        else:
            obstacle = min(ult[0],ult[1])
        if obstacle <= distanceSecu:# and obstacle !=0:
            print("obstable",obstacle)
            u[0,0],u[1,0] = 0,0
            ob = 1
            if time.time() - t0 >= 5:
                u[0,0],u[1,0] = -120,-120
        if ob == 0:
            t = time.time()
        return u,t
    else :
        t = time.time()
        return u0,t

def detectObstacleAr(rob,u0,mode,t0):
    ob = 0
    t = t0
    if mode == 1:
        u = u0.copy()
        obstacle = rob.ultrason('p')[0]
        if obstacle <= distanceSecu:# and obstacle !=0:
            print("obstable",obstacle)
            u[0,0],u[1,0] = 0,0
        ult = rob.ultrason('b')
        obstacle = min(ult[0],ult[1])
        if obstacle <= distanceSecu:# and obstacle !=0:
            print("obstable",obstacle)
            u[0,0],u[1,0] = 0,0
        return u,t
    else:
        t = time.time()
        return u0,t
        

    
    

def deplacement(rob,a,b,mode = 0):
    posx = []
    posy = []
    postheta = []
    X = np.array([[rob.x],[rob.y],[rob.theta]])
    m = X[0:2].reshape((2,1))
    L0,R0 = rob.odometer()
    u = np.array([[0],[0]])
    t0  = time.time()
    t1 = time.time()
    t = time.time()
    print(t)
    while(time.time() - t0 < 100):
        if (time.time() - t1 > dt):
            L1,R1 = rob.odometer()
            rob = maj(rob, L1-L0,R1-R0)
            L0,R0 = L1,R1
            X = np.array([[rob.x],[rob.y],[rob.theta]])
            m = X[0:2].reshape((2,1))
            u = control(X,a,b)

            u,t = detectObstacleAv(rob,u,mode,t)
            
            '''
            if mode >= 1:
                obstacle = rob.ultrason('o')[0]
                if obstacle <= distanceSecu:# and obstacle !=0:
                    print("obstable",obstacle)
                    u[0,0],u[1,0] = 0,0
                ult = rob.ultrason('f')
                if mode == 2:
                    obstacle = ult[1]
                else:
                    obstacle = min(ult[0],ult[1])
                if obstacle <= distanceSecu:# and obstacle !=0:
                    print("obstable",obstacle)
                    u[0,0],u[1,0] = 0,0
            '''
                
            if np.linalg.norm(m-b) < 50:
                break
            rob.Motor(int(u[0,0]),int(u[1,0]))
            posx.append(rob.x)
            posy.append(rob.y)
            postheta.append(rob.theta)
            t1 = time.time()

        
    rob.Motor(0,0)
    return np.array(posx),np.array(posy),np.array(postheta)

def deplacementX(rob,a,b,mode = 0):
    posx = []
    posy = []
    postheta = []
    X = np.array([[rob.x],[rob.y],[rob.theta]])
    m = X[0:2].reshape((2,1))
    L0,R0 = rob.odometer()
    u = np.array([[0],[0]])
    t0  = time.time()
    t1 = time.time()
    t= time.time()
    while(time.time() - t0 < 100):
        if (time.time() - t1 > dt):
            L1,R1 = rob.odometer()
            rob = maj(rob, L1-L0,R1-R0)
            L0,R0 = L1,R1
            X = np.array([[rob.x],[rob.y],[rob.theta]])
            m = X[0:2].reshape((2,1))
            u = control(X,a,b)
            u,t = detectObstacleAv(rob,u,mode,t)
            '''
            if mode >= 1:
                obstacle = rob.ultrason('o')[0]
                if obstacle <= distanceSecu:# and obstacle !=0:
                    print("obstable",obstacle)
                    u[0,0],u[1,0] = 0,0
                ult = rob.ultrason('f')
                if mode == 2:
                    obstacle = ult[1]
                else:
                    obstacle = min(ult[0],ult[1])
                if obstacle <= distanceSecu:# and obstacle !=0:
                    print("obstable",obstacle)
                    u[0,0],u[1,0] = 0,0
            
            '''
            if abs(rob.x - b[0,0]) <50:
                break
            rob.Motor(int(u[0,0]),int(u[1,0]))
            posx.append(rob.x)
            posy.append(rob.y)
            postheta.append(rob.theta)
            t1 = time.time()

        
    rob.Motor(0,0)
    return np.array(posx),np.array(posy),np.array(postheta)

def deplacementY(rob,a,b,mode = 0):
    posx = []
    posy = []
    postheta = []
    X = np.array([[rob.x],[rob.y],[rob.theta]])
    m = X[0:2].reshape((2,1))
    L0,R0 = rob.odometer()
    u = np.array([[0],[0]])
    t0  = time.time()
    t1 = time.time()
    t = time.time()
    while(time.time() - t0 < 100):
        if (time.time() - t1 > dt):
            L1,R1 = rob.odometer()
            rob = maj(rob, L1-L0,R1-R0)
            L0,R0 = L1,R1
            X = np.array([[rob.x],[rob.y],[rob.theta]])
            m = X[0:2].reshape((2,1))
            u = control(X,a,b)
            u,t = detectObstacleAv(rob,u,mode,t)
            '''
            if mode >= 1:
                obstacle = rob.ultrason('o')[0]
                if obstacle <= distanceSecu:# and obstacle !=0:
                    print("obstable",obstacle)
                    u[0,0],u[1,0] = 0,0
                ult = rob.ultrason('f')
                if mode == 2:
                    obstacle = ult[1]
                else:
                    obstacle = min(ult[0],ult[1])
                if obstacle <= distanceSecu:# and obstacle !=0:
                    print("obstable",obstacle)
                    u[0,0],u[1,0] = 0,0
            '''
            if abs(rob.y - b[1,0]) <50:
                break
            rob.Motor(int(u[0,0]),int(u[1,0]))
            posx.append(rob.x)
            posy.append(rob.y)
            postheta.append(rob.theta)
            t1 = time.time()

        
    rob.Motor(0,0)
    return np.array(posx),np.array(posy),np.array(postheta)

def deplacementAr(rob,a,b,mode=0):
    posx = []
    posy = []
    postheta = []
    X = np.array([[rob.x],[rob.y],[rob.theta]])
    m = X[0:2].reshape((2,1))
    L0,R0 = rob.odometer()
    u = np.array([[0],[0]])
    t0  = time.time()
    t1 = time.time()
    while(time.time() - t0 < 100):
        if (time.time() - t1 > dt):
            L1,R1 = rob.odometer()
            rob = maj(rob, L1-L0,R1-R0)
            L0,R0 = L1,R1
            X = np.array([[rob.x],[rob.y],[rob.theta]])
            m = X[0:2].reshape((2,1))
            u = controlAr(X,a,b)

            u,t = detectObstacleAr(rob,u,mode,t)
            '''
            if mode == 1:
                obstacle = rob.ultrason('p')[0]
                if obstacle <= distanceSecu:# and obstacle !=0:
                    print("obstable",obstacle)
                    u[0,0],u[1,0] = 0,0
                ult = rob.ultrason('b')
                obstacle = min(ult[0],ult[1])
                if obstacle <= distanceSecu:# and obstacle !=0:
                    print("obstable",obstacle)
                    u[0,0],u[1,0] = 0,0
            '''
                
            if np.linalg.norm(m-b) < 50:
                break
            rob.Motor(int(u[0,0]),int(u[1,0]))
            posx.append(rob.x)
            posy.append(rob.y)
            postheta.append(rob.theta)
            t1 = time.time()

        
    rob.Motor(0,0)
    return np.array(posx),np.array(posy),np.array(postheta)

def deplacementArY(rob,a,b,mode =0):
    posx = []
    posy = []
    postheta = []
    X = np.array([[rob.x],[rob.y],[rob.theta]])
    m = X[0:2].reshape((2,1))
    L0,R0 = rob.odometer()
    u = np.array([[0],[0]])
    t0  = time.time()
    t1 = time.time()
    t = time.time()
    while(time.time() - t0 < 100):
        if (time.time() - t1 > dt):
            L1,R1 = rob.odometer()
            rob = maj(rob, L1-L0,R1-R0)
            L0,R0 = L1,R1
            X = np.array([[rob.x],[rob.y],[rob.theta]])
            m = X[0:2].reshape((2,1))
            u = controlAr(X,a,b)
            u,t = detectObstacleAr(rob,u,mode,t)
            '''
            if mode == 1:
                obstacle = rob.ultrason('p')[0]
                if obstacle <= distanceSecu:# and obstacle !=0:
                    print("obstable",obstacle)
                    u[0,0],u[1,0] = 0,0
                ult = rob.ultrason('b')
                obstacle = min(ult[0],ult[1])
                if obstacle <= distanceSecu:# and obstacle !=0:
                    print("obstable",obstacle)
                    u[0,0],u[1,0] = 0,0
            '''
            if abs(rob.y - b[1,0]) <50:
                break
            rob.Motor(int(u[0,0]),int(u[1,0]))
            posx.append(rob.x)
            posy.append(rob.y)
            postheta.append(rob.theta)
            t1 = time.time()

        
    rob.Motor(0,0)
    return np.array(posx),np.array(posy),np.array(postheta)


def deplacementArX(rob,a,b,mode =0):
    posx = []
    posy = []
    postheta = []
    X = np.array([[rob.x],[rob.y],[rob.theta]])
    m = X[0:2].reshape((2,1))
    L0,R0 = rob.odometer()
    u = np.array([[0],[0]])
    t0  = time.time()
    t1 = time.time()
    t = time.time()
    while(time.time() - t0 < 100):
        if (time.time() - t1 > dt):
            L1,R1 = rob.odometer()
            rob = maj(rob, L1-L0,R1-R0)
            L0,R0 = L1,R1
            X = np.array([[rob.x],[rob.y],[rob.theta]])
            m = X[0:2].reshape((2,1))
            u = controlAr(X,a,b)
            u,t = detectObstacleAr(rob,u,mode,t)
            '''
            if mode == 1:
                obstacle = rob.ultrason('p')[0]
                if obstacle <= distanceSecu:# and obstacle !=0:
                    print("obstable",obstacle)
                    u[0,0],u[1,0] = 0,0
                ult = rob.ultrason('b')
                obstacle = min(ult[0],ult[1])
                if obstacle <= distanceSecu:# and obstacle !=0:
                    print("obstable",obstacle)
                    u[0,0],u[1,0] = 0,0
            '''
            if abs(rob.x - b[0,0]) <50:
                break
            rob.Motor(int(u[0,0]),int(u[1,0]))
            posx.append(rob.x)
            posy.append(rob.y)
            postheta.append(rob.theta)
            t1 = time.time()
        
    rob.Motor(0,0)
    return np.array(posx),np.array(posy),np.array(postheta)

def deplacementAngle(rob,angle,precision = 0.4):
    posx = []
    posy = []
    postheta = []
    X = np.array([[rob.x],[rob.y],[rob.theta]])
    m = X[0:2].reshape((2,1))
    L0,R0 = rob.odometer()

    u = np.array([[0],[0]])
    t0  = time.time()
    t1 = time.time()
    while(time.time() - t0 < 100):
        if (time.time() - t1 > dt):
            L1,R1 = rob.odometer()
            rob = maj(rob, L1-L0,R1-R0)
            L0,R0 = L1,R1
            X = np.array([[rob.x],[rob.y],[rob.theta]])
            m = X[0:2].reshape((2,1))
            u = controlangle(X,angle)
            rob.Motor(int(u[0,0]),int(u[1,0]))
            posx.append(rob.x)
            posy.append(rob.y)
            postheta.append(np.pi*signal.sawtooth(rob.theta+np.pi))
            if abs(np.pi*signal.sawtooth(angle-X[2,0]+np.pi)) < precision:
                print("end")
                break
            t1 = time.time()
    rob.Motor(0,0)
    return np.array(posx),np.array(posy),np.array(postheta)



def recalageMurDroit(rob):
    UAv, UAr = rob.ultrason('r')
    print(UAv,UAr)
    if UAv > UAr:
        while UAv >UAr+8:
            rob.Motor(140,-140)
            UAv,UAr = rob.ultrason('r')
    else:
        while UAr >UAv+8:
            rob.Motor(-140,140)
            UAv,UAr = rob.ultrason('r')
    rob.Motor(0,0)
    print(UAv,UAr)

def recalageMurGauche(rob):
    UAv, UAr = rob.ultrason('r')
    print(UAv,UAr)
    if UAv > UAr:
        while UAv >UAr+8:
            rob.Motor(-150,150)
            UAv,UAr = rob.ultrason('r')
    else:
        while UAr >UAv+8:
            rob.Motor(150,-150)
            UAv,UAr = rob.ultrason('r')
    rob.Motor(0,0)
    print(UAv,UAr)


def recalageMurAr(rob):
    UG, UD = rob.ultrason('b')
    print(UG,UD)
    if UG > UD:
        while UG >UD+8:
            rob.Motor(-150,150)
            UG,UD = rob.ultrason('b')
    else:
        while UD >UG+8:
            rob.Motor(150,-150)
            UG,UD = rob.ultrason('b')
    rob.Motor(0,0)
    print(UG,UD)

def recalageMurAvant(rob):
    UG, UD = rob.ultrason('b')
    print(UG,UD)
    if UG > UD:
        while UG >UD+8:
            rob.Motor(150,-150)
            UG,UD = rob.ultrason('b')
    else:
        while UD >UG+8:
            rob.Motor(-150,150)
            UG,UD = rob.ultrason('b')
    rob.Motor(0,0)
    print(UG,UD)


def recalageLidar(rob,angle):
    print('#####################################')
    ##('5 tour = 32 sec')
    rob.theta = angle
    
    rob.majLidar()
    X = np.array([[rob.x],[rob.y],[rob.theta]])
    er = np.pi*signal.sawtooth(angle-X[2,0]+np.pi)
    u1 = -sign(er)*150
    u2 = sign(er)*150
    rob.Motor(int(u1),int(u2))
    time.sleep(abs(er)*1)
    rob.Motor(0,0)
    time.sleep(0.5)
    rob.theta = angle
    rob.majLidar()
    X = np.array([[rob.x],[rob.y],[rob.theta]])
    er = np.pi*signal.sawtooth(angle-X[2,0]+np.pi)
    u1 = -sign(er)*150
    u2 = sign(er)*150
    rob.Motor(int(u1),int(u2))
    time.sleep(abs(er)*1)
    rob.Motor(0,0)
    time.sleep(0.5)
    print('#####################################')

def recalageGold(rob):
    posGold = rob.positionGold()
    reference =  200 # entre 258 et 249
    distance = reference - posGold
    while distance > 5:
        rob.Motor(120,120)
        time.sleep(0.2)
        rob.Motor(0,0)
        posGold = rob.positionGold()
        if posGold != 0: 
            distance = reference - posGold
    while distance < -5:
        rob.Motor(-120,-125)
        time.sleep(0.2)
        rob.Motor(0,0)
        posGold = rob.positionGold()
        if posGold != 0:
            distance = reference - posGold

    rob.Motor(0,0)

def recalagePaletAPousser(rob):
    posPalet = rob.positionPalet()
    reference =  208 # entre 258 et 249
    distance = reference - posPalet
    while distance > 0 :
        rob.Motor(-120,-120)
        posPalet = rob.positionPalet()
        distance = reference - posGold
    rob.Motor(0,0)

    
    time.sleep(1)
    posPalet = rob.positionPalet()
    reference =  214 # entre 258 et 249
    distance = reference - posPalet
    while distance < 0 :
        rob.Motor(120,120)
        posPalet = rob.positionPalet()
        distance = reference - posGold
    rob.Motor(0,0)
