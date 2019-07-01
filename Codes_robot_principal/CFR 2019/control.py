import time
import terminatom2 as tm
import matplotlib.pyplot as plt 
import numpy as np
import pygame
from scipy import signal
from pygame.locals import *



pygame.init()
screen = pygame.display.set_mode((200,200))
pygame.display.set_caption("terminatom")
background = pygame.Surface(screen.get_size())
r = 39
alpha1 = 0.3
alpha2 = 0.3
l = 310
V = 120
dt = 0.05
K = 3
a= np.array([[640]  ,
          [3000-425]  ])

b = np.array([[640],
           [600]])


def sign(a):
    if a >= 0:
        return 1
    else:
        return -1

def controlManuel(u):
    u1 = u[0,0]
    u2 = u[1,0]
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_z:
                u1 = 300
                u2 = 300
            elif event.key == K_s:
                u1 = -300
                u2 = -300
            elif event.key == K_q:
                u1 = -150
                u2 = 150
            elif event.key == K_d:
                u1 = 150
                u2 = -150
            elif event.key == K_b:
                u1 = 0
                u2 = 0
            elif event.key== K_k:
                pygame.quit()
                u1 = 1000
    return np.array([ [u1],[u2]])


def controlTrajTest(t0):
    u1,u2 = 0,0
    if(time.time() - t0 < 14.5):
        u1 = 120
        u2 = -120
    elif (time.time() -t0 < 6):
        u1 = 120
        u2 = 120
    else:
        u1 = 0
        u2 = 0
    return np.array([ [u1],[u2]])


def control(x):
    phi = np.arctan2(b[1,0]-a[1,0],b[0,0]-a[0,0])
    m = x[0:2].reshape((2,1))
    e = np.linalg.det(np.hstack((b-a,m-a)))/np.linalg.norm(b-a)
    thetabar = phi - np.arctan(e)
    angle = K*np.arctan(np.tan(( thetabar -x [2,0] )/2))
    u2 = (angle*l/r*alpha1 + 2*V)* 0.5
    u1 = 2*V - u2
    er.append(np.arctan(e))
    return np.array([ [u1],[u2]])




def controlangle(x,angle):
    er = np.arctan(np.tan(( angle -x [2,0] )))
    print('---------------------')
    print(angle, x[2,0], er)
    coef = er*2/np.pi
    print(coef)
    u1 = -sign(er)*90
    u2 = sign(er)*90
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
    
def deplacement(rob,a,b):
    posx = []
    posy = []
    postheta = []
    X = np.array([[rob.x],[rob.y],[rob.theta]])
    m = X[0:2].reshape((2,1))
    
    L0,R0 = rob.odometer()

    u = np.array([[0],[0]])
    t0  = time.time()
    t1 = time.time()
    while(time.time() - t0 < 200):
        if (time.time() - t1 > dt):
            L1,R1 = rob.odometer()
            rob = maj(rob, L1-L0,R1-R0)
            L0,R0 = L1,R1
            X = np.array([[rob.x],[rob.y],[rob.theta]])
            m = X[0:2].reshape((2,1))
            u = controlManuel(u)
            if u[0,0] == 1000:
                break
            rob.Motor(int(u[0,0]),int(u[1,0]))
            posx.append(rob.x)
            posy.append(rob.y)
            postheta.append(rob.theta)
            t1 = time.time()
        #else:
        #    print("jai le teeeemppppssss")
    rob.Motor(0,0)
    return np.array(posx),np.array(posy),np.array(postheta)


screen.blit(background, (0,0))
pygame.display.flip()






rob = tm.terminatom(275,275,np.pi/2)
er = []
x,y,theta = deplacement(rob,a,b)

plt.figure(1)
plt.axis('equal')
drawplateau()
plt.plot(a[0,0],a[1,0],'bo')
for i in range(1,len(x)):
    plt.plot(x[i],y[i],'ro')
plt.show()
