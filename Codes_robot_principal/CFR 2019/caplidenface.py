# -*- coding: utf-8 -*-
"""
Created on Tue May 21 17:38:56 2019

@author: jongo
"""

from rplidar import RPLidar
import numpy as np
from scipy import signal

rayon_recherche = 300
"""
Connexion et deconnexion au Lidar
"""        
    
def connect():
    lidar = RPLidar('/dev/ttyUSB0')

    info = lidar.get_info()
    print(info)

    health = lidar.get_health()
    print(health)
    return lidar

def disconnect():
    lidar = RPLidar('/dev/ttyUSB0')
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()


"""
Localisation du robot
"""

def dep_zones(x,y,theta,zones):
    zones_f = zones.copy()
    depx = x
    depy = y
    zones_f[0,:] = zones_f[0,:]-x
    zones_f[1,:] = zones_f[1,:]-y
    mat = np.array([[np.cos(-theta),-np.sin(-theta)],[np.sin(-theta),np.cos(-theta)]])
    for i in range(len(zones[0])):
        bal = np.dot(mat,(zones_f[:,i].reshape(2,1)))
        zones_f[0,i] = bal[0,0]
        zones_f[1,i] = bal[1,0]
    print(zones_f)
    return(zones_f,depx,depy)
    
def repere(balises,depx,depy,theta):
    lidar = RPLidar('/dev/ttyUSB0')
    abscisse = []
    ordonnee = []
    x_v = []
    y_v = []
    for i, scan in enumerate(lidar.iter_measurments()):
        #print(i,scan)
        valeur = scan[1]
        angle = scan[2]*2*np.pi/360
        x = -scan[3] * np.cos(angle + np.pi/2)
        y = scan[3] * np.sin(angle + np.pi/2)
        x_v.append(x)
        y_v.append(y)
        if valeur == 15 and test_zone(x,y,balises):
            abscisse.append(x)
            ordonnee.append(y)
        if i>=2000 :
            lidar.stop()
            lidar.disconnect()
            balise1,balise2,balise3,balise4 = pos_balises(abscisse,ordonnee,balises,depx,depy,theta)
            return(balise1,balise2,balise3,balise4)
        
def pos_balises(abscisse,ordonnee,balises,depx,depy,theta):
    balise_1 = []
    balise_2 = []
    balise_3 = []
    balise_4 = []
    b1 = np.zeros((2,1))
    b2 = np.zeros((2,1))
    b3 = np.zeros((2,1))
    b4 = np.zeros((2,1))
    mat = np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
    for i in range(len(abscisse)):
        if test_zone(abscisse[i],ordonnee[i],balises[:,0].reshape(2,1)):
            balise_1.append([abscisse[i],ordonnee[i]])
        if test_zone(abscisse[i],ordonnee[i],balises[:,1].reshape(2,1)):
            balise_2.append([abscisse[i],ordonnee[i]])
        if test_zone(abscisse[i],ordonnee[i],balises[:,2].reshape(2,1)):
            balise_3.append([abscisse[i],ordonnee[i]])
        if test_zone(abscisse[i],ordonnee[i],balises[:,3].reshape(2,1)):
            balise_4.append([abscisse[i],ordonnee[i]])
    if balise_1 != []:
        b1[0,0] = np.mean(np.array(balise_1)[:,0])
        b1[1,0] = np.mean(np.array(balise_1)[:,1])
        b1 = np.dot(mat,b1)+np.array([[depx],[depy]])
    if balise_2 != []:
        b2[0,0] = np.mean(np.array(balise_2)[:,0])
        b2[1,0] = np.mean(np.array(balise_2)[:,1])
        b2 = np.dot(mat,b2)+np.array([[depx],[depy]])
    if balise_3 != []:
        b3[0,0] = np.mean(np.array(balise_3)[:,0])
        b3[1,0] = np.mean(np.array(balise_3)[:,1])
        b3 = np.dot(mat,b3)+np.array([[depx],[depy]])
    if balise_4 != []:
        b4[0,0] = np.mean(np.array(balise_4)[:,0])
        b4[1,0] = np.mean(np.array(balise_4)[:,1])
        b4 = np.dot(mat,b4)+np.array([[depx],[depy]])
    print(b1,b2,b3,b4)
    return(b1,b2,b3,b4)

def test_zone(x,y,zones):
    r = rayon_recherche
    flag = False
    for i in range(len(zones[0])):
        dist = np.sqrt((x-zones[0,i])**2+(y-zones[1,i])**2)
        if dist < r :
            flag = True
            return(flag)
    return(flag)
    
def local(x,y,bal1,bal2,bal3,bal4):
    test = False
    balises_reelles = np.array([[60,1940,-220,1000],[3080,3080,1500,-80]])   #Positions exactes dans le repere
    rbal = 40
    balises_approx = balises_reelles.copy()
    
    balises_approx[0,0] = balises_approx[0,0] + rbal * np.cos(np.arctan2(y-balises_reelles[1,0],x-balises_reelles[0,0])) 
    balises_approx[1,0] = balises_approx[1,0] + rbal * np.sin(np.arctan2(y-balises_reelles[1,0],x-balises_reelles[0,0]))
    balises_approx[0,1] = balises_approx[0,1] + rbal * np.cos(np.arctan2(y-balises_reelles[1,1],x-balises_reelles[0,1])) 
    balises_approx[1,1] = balises_approx[1,1] + rbal * np.sin(np.arctan2(y-balises_reelles[1,1],x-balises_reelles[0,1]))
    
    d1 = np.sqrt((y-bal1[1])**2+(x-bal1[0])**2)
    d2 = np.sqrt((y-bal2[1])**2+(x-bal2[0])**2)
    d3 = np.sqrt((y-bal3[1])**2+(x-bal3[0])**2)
    d4 = np.sqrt((y-bal4[1])**2+(x-bal4[0])**2)
    #if y >= 1500:
    if x <= 950:
        if bal2[0]!=0 and bal1[0] !=0:
            b = np.sqrt((abs(bal1[1])-abs(bal2[1]))**2+(abs(bal1[0])-abs(bal2[0]))**2)
            al_kashi = np.arccos(max((d1**2+b**2-d2**2)/(2*d1*b),-1))
            xf = d1*np.cos(al_kashi)+balises_approx[0,0]
            yf = -d1*np.sin(al_kashi)+balises_approx[1,0]
            angle1 = np.arctan2(yf-bal1[1],xf-bal1[0])
            print(angle1*360/2/np.pi)
            angle2 = np.arctan2(yf-balises_approx[1,0],xf-balises_approx[0,0])
            print(angle2*360/2/np.pi)
            angle = angle2 - angle1
            test = True
        else :
            print("aie aie aie")
            b =np.sqrt((abs(bal1[1])-abs(bal3[1]))**2+(abs(bal1[0])-abs(bal3[0]))**2)
            al_kashi = np.arccos(max((d1**2+b**2-d3**2)/(2*d1*b),-1))
            xf = d1*np.cos(al_kashi)+balises_approx[0,0]
            yf = d1*np.sin(al_kashi)+balises_approx[1,0]
            angle1 = np.arctan2(yf-bal1[1],xf-bal1[0])
            #print(angle1*360/2/pi)
            angle2 = np.arctan2(yf-balises_approx[1,0],xf-balises_approx[0,0])
            #print(angle2*360/2/pi)
            angle = angle2 - angle1
    else :
        if bal1[0] != 0:
            b =np.sqrt((abs(bal1[1])-abs(bal2[1]))**2+(abs(bal1[0])-abs(bal2[0]))**2)
            al_kashi = np.arccos(max((d2**2+b**2-d1**2)/(2*d2*b),-1))
            xf = -d2*np.cos(al_kashi)+balises_approx[0,1]
            yf = -d2*np.sin(al_kashi)+balises_approx[1,1]
            angle1 = np.arctan2(yf-bal2[1],xf-bal2[0])
            angle2 = np.arctan2(yf-balises_approx[1,1],xf-balises_approx[0,1])
            angle = angle2 - angle1
            test = True
        else:
            xf,yf,angle = 0,0,0
                
    '''
    else : 
        b =np.sqrt((abs(bal3[1])-abs(bal4[1]))**2+(abs(bal3[0])-abs(bal4[0]))**2)
        al_kashi = np.arccos((d4**2+b**2-d3**2)/(2*d4*b))
        xf = d4*np.sin(al_kashi)+balises_approx[0,3]-100
        yf = -d4*np.cos(al_kashi)+balises_approx[1,3]
    '''
    norm1 = np.sqrt((balises_approx[0,0]-bal1[0])**2+(balises_approx[1,0]-bal1[1])**2)
    norm2 = np.sqrt((balises_approx[0,1]-bal2[0])**2+(balises_approx[1,1]-bal2[1])**2)
    if (bal1[0] == 0) or (bal2[0] == 0)or (norm1 >300) or (norm2 >300):
        test = False
    
    return(xf,yf,angle,test)
    
def main(x,y,cap):
    balises_reelles = np.array([[100,1900,-200,1000],[3030,3030,1500,-30]])   #Positions exactes dans le repere
    theta = cap + 0.52
    zones_rech = balises_reelles.copy()  #Positions des balises par rapport au robot = zones de recherches
    test = False
    rayon_recherche = 300
    tentative = 0
    while test == False:
        print(x,y,cap)
        zones_rech,depx,depy = dep_zones(x,y,theta,zones_rech) # Mise a  jour des zones de recherches
        #print("zones de recherche :",zones_rech)
        bal1,bal2,bal3,bal4 = repere(zones_rech,depx,depy,theta)
        xf, yf, angle, test = local(x,y,bal1,bal2,bal3,bal4)
        #print(xf,yf)
        #print((cap+angle)*360/2/np.pi)
        tentative = tentative +1
        if tentative > 2:
            xf,yf,angle = [x],[y],[0]
            rayon_recherche = rayon_recherche +50
            break
        
    return (xf,yf,np.pi*signal.sawtooth(cap+angle+np.pi/2+np.pi))


if __name__ =="__main__":
    print("debut")
    connect()
    print(main(290,290,-np.pi))
