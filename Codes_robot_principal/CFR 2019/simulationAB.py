from roblib import *


def drawplateau():
    p = np.array([[0,2000,2000,0,0],
                   [3000,3000,0,0,3000]])
    plot2D(p,'black')


def f(x,u):
    dx =  (r*alpha1*u[0,0]+r*alpha2*u[1,0])*np.cos(x[2,0])/2
    dy =  (r*alpha1*u[0,0]+r*alpha2*u[1,0])*np.sin(x[2,0])/2
    dtheta = (r*alpha1*u[1,0]-r*alpha2*u[0,0])/l
    print(dx,dy,dtheta)
    return array([ [dx],[dy],[dtheta]])

    
x = array([ [1000],[0],[pi/2]])
dt  = 0.01


pa= array([[1000]  ,
          [0]  ])

pb = array([[1000],
           [2000]])

r= 3.6
alpha1 = 5*0.26
alpha2 =5*0.26
l = 17
ax=init_figure(-400,4000,-400,4000)
thetabar = -1+2*pi
m = x[0:2].reshape((2,1))
V = 120

a = pa[:,0].reshape((2,1))
b = pb[:,0].reshape((2,1))
i = 0



def control(x):
    phi = arctan2(b[1,0]-a[1,0],b[0,0]-a[0,0])
    m = x[0:2].reshape((2,1))
    e = det(hstack((b-a,m-a)))/norm(b-a)
    thetabar = phi - arctan(e)
    angle = arctan(tan(( thetabar -x [2,0] )/2))
    u2 = (angle*l/r*alpha1 + 2*V)* 0.5
    u1 = 2*V - u2
    return array([ [u1],[u2]])
    
    


for t in arange(0,200,dt):
    clear(ax)

    a = pa[:,i].reshape((2,1))
    b = pb[:,i].reshape((2,1))
    draw_tank(x,'darkblue',30)
    plot2D(hstack((pa,pb)),'red')
    plot2D(pa,'ro')
    plot2D(pb,'ro')
    drawplateau()
    u = control(x)
    x   =x+dt*f(x,u)
    m = x[0:2].reshape((2,1))
    if (norm(m-b) < 100):
        break    
