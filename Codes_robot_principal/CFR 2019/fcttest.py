import time
import terminatom as tm
import matplotlib.pyplot as plt 
import numpy as np

def avanceDroit(rob,vitesse):
    L0,R0 = rob.odometer()
    rob.Motor(vitesse,vitesse)
    ListError = []
    t0 = time.time()
    erreur = 0
    tstart = time.time()
    while (time.time()-t0 < 6):
        if (time.time() - tstart > 0.01):
            #print("hey")
            L1,R1 = rob.odometer()
            el = L1-L0
            er = R1-R0
            erreur = el-er
            ListError.append(erreur)
            #print("erreur = ",erreur)
            if erreur > 0:
                erreur = min( int(erreur), 20)
            else:
                erreur = max( int(erreur), -20)
            rob.Motor(vitesse - int(erreur), vitesse + int(erreur))
            tstart = time.time()
    rob.Motor(0,0)

    
    print("erreure finale :",erreur)
    return ListError

def test(rob):
    rob.Motor(100,100)
    time.sleep(4)
    rob.Motor(0,0)



r = 3.6
alpha1 = 0.3
alpha2 = 0.3
l = 17
V = 120
dt = 0.1
a= np.array([[1000]  ,
          [0]  ])

b = np.array([[1000],
           [2000]])


def f(rob):
    dx =  (r*alpha1*u[0,0]+r*alpha2+u[1,0])*np.cos(x[2,0])/2
    dy =  (r*alpha1*u[0,0]+r*alpha2+u[1,0])*np.sin(x[2,0])/2
    dtheta = (r*alpha1*u[1,0]+r*alpha2+u[0,0])/l

def control(x):
    phi = np.arctan2(b[1,0]-a[1,0],b[0,0]-a[0,0])
    m = x[0:2].reshape((2,1))
    e = np.linalg.det(np.hstack((b-a,m-a)))/np.linalg.norm(b-a)
    thetabar = phi - np.arctan(e)
    angle = np.arctan(np.tan(( thetabar -x [2,0] )/2))
    u2 = (angle*l/r*alpha1 + 2*V)* 0.5
    u1 = 2*V - u2
    er.append(np.arctan(e))
    return np.array([ [u1],[u2]])

def maj(rob,encodG,encodD):
    v1 = encodG*39*2*np.pi/1024
    v2 = encodD*39*2*np.pi/1024
    dx = (v1+v2)*np.cos(rob.theta)/2
    dy = (v1+v2)*np.sin(rob.theta)/2
    dtheta = (v2-v1)/l
    rob.x = rob.x + dt*dx
    rob.y = rob.y + dt*dy
    rob.theta = rob.theta + dt*dtheta
    return rob
    

def deplacement(rob,a,b):
    posx = []
    posy = []
    postheta = []
    x = np.array([[rob.x],[rob.y],[rob.theta]])
    m = x[0:2].reshape((2,1))
    t0  = time.time()
    t1 = time.time()
    L0,R0 = rob.odometer()
    rob.x = 1000
    while(time.time() - t0 < 6):
        if (time.time() - t1 > dt):
            L1,R1 = rob.odometer()
            rob = maj(rob, L1-L0,R1-R0)
            L0,R0 = L1,R1
            x = np.array([[rob.x],[rob.y],[rob.theta]])
            m = x[0:2].reshape((2,1))
            u = control(x)
            rob.Motor(int(u[0,0]),int(u[1,0]))
            posx.append(rob.x)
            posy.append(rob.y)
            postheta.append(rob.theta)
            t1 = time.time()
            
        if (np.linalg.norm(m-b) < 100):
            break
    rob.Motor(0,0)
    return np.array(posx),np.array(posy),np.array(postheta)


rob = tm.terminatom()
er = []

avanceDroit(rob,150)
'''
x,y,theta = deplacement(rob,a,b)
t= np.linspace(0,6,len(theta))
plt.figure(1)
plt.plot(x,y,'ro')
plt.figure(2)
plt.plot(t,theta)
plt.figure(3)
er = np.array(er)
plt.plot(t,er)
plt.show()
'''
