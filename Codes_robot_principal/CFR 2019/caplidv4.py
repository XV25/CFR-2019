# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 14:10:36 2019

@author: jongo
"""

from rplidar import RPLidar
import matplotlib.pyplot as plt
import time 
import numpy as np



"""
Connexion et deconnexion au Lidar
"""

def connect(addr):
    lidar = RPLidar(addr)

    info = lidar.get_info()
    #print(info)

    health = lidar.get_health()
    #print(health)
    return lidar

def disconnect(lidar):
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()


"""
Localisation du robot
"""

def dep_zones(x,y,theta,zones):
    xrob = 0  #Position initiale du robot
    yrob = 0
    zones_f = zones.copy()
    depx = x-xrob
    depy = y-yrob
    zones_f[0,:] = zones_f[0,:]-depx
    zones_f[1,:] = zones_f[1,:] -depy
    mat = np.array([[np.cos(-theta),-np.sin(-theta)],[np.sin(-theta),np.cos(-theta)]])
    for i in range(len(zones[0])):
        bal = np.dot(mat,(zones_f[:,i].reshape(2,1)-np.array([[xrob],[yrob]])))  +np.array([[xrob],[yrob]])
        zones_f[0,i] = bal[0,0]
        zones_f[1,i] = bal[1,0]
    return(zones_f,depx,depy)
    
def repere(lidar,balises,depx,depy,theta):
    xrob = 0  #Position initiale du robot
    yrob = 0
    abscisse = []
    ordonnee = []
    x_v = []
    y_v = []
    for i, scan in enumerate(lidar.iter_measurments()):
        valeur = scan[1]
        angle = scan[2]*2*np.pi/360
        x = -scan[3] * np.cos(angle + np.pi/2) + xrob
        y = scan[3] * np.sin(angle + np.pi/2) + yrob
        x_v.append(x)
        y_v.append(y)
        if valeur == 15 and test_zone(x,y,balises):
            abscisse.append(x)
            ordonnee.append(y)
        if i>=500 :
            lidar.stop()
            lidar.disconnect()
            balise1,balise2,balise3,balise4 = pos_balises(abscisse,ordonnee,balises,depx,depy,theta)
            return(balise1,balise2,balise3,balise4)
        
def pos_balises(abscisse,ordonnee,balises,depx,depy,theta):
    xrob = 0  #Position initiale du robot
    yrob = 0
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
        b1 = np.dot(mat,(b1-np.array([[xrob],[yrob]]))) +np.array([[xrob],[yrob]]) +np.array([[depx],[depy]])
    if balise_2 != []:
        b2[0,0] = np.mean(np.array(balise_2)[:,0])
        b2[1,0] = np.mean(np.array(balise_2)[:,1])
        b2 = np.dot(mat,(b2-np.array([[xrob],[yrob]]))) +np.array([[xrob],[yrob]]) +np.array([[depx],[depy]])
    if balise_3 != []:
        b3[0,0] = np.mean(np.array(balise_3)[:,0])
        b3[1,0] = np.mean(np.array(balise_3)[:,1])
        b3 = np.dot(mat,(b3-np.array([[xrob],[yrob]]))) +np.array([[xrob],[yrob]]) +np.array([[depx],[depy]])
    if balise_4 != []:
        b4[0,0] = np.mean(np.array(balise_4)[:,0])
        b4[1,0] = np.mean(np.array(balise_4)[:,1])
        b4 = np.dot(mat,(b4-np.array([[xrob],[yrob]]))) +np.array([[xrob],[yrob]]) +np.array([[depx],[depy]])
    return(b1,b2,b3,b4)

def test_zone(x,y,zones):
    r = 150
    flag = False
    for i in range(len(zones[0])):
        dist = np.sqrt((x-zones[0,i])**2+(y-zones[1,i])**2)
        if dist < r :
            flag = True
            return(flag)
    return(flag)
    
def local(x,y,bal1,bal2,bal3,bal4):
    balises_reelles = np.array([[100,1900,-60,1000],[-30,-30,1500,3020]])   #Positions exactes dans le repère
    d1 = np.sqrt((y-bal1[1])**2+(x-bal1[0])**2)
    d2 = np.sqrt((y-bal2[1])**2+(x-bal2[0])**2)
    d3 = np.sqrt((y-bal3[1])**2+(x-bal3[0])**2)
    d4 = np.sqrt((y-bal4[1])**2+(x-bal4[0])**2)
    if y <= 1500:
        if x <= 950:
            b =np.sqrt((abs(bal1[1])-abs(bal2[1]))**2+(abs(bal1[0])-abs(bal2[0]))**2)
            al_kashi = np.arccos(max((d1**2+b**2-d2**2)/(2*d1*b),-1))
            xf = d1*np.cos(al_kashi)+balises_reelles[0,0]
            yf = d1*np.sin(al_kashi)+balises_reelles[1,0]
            angle1 = np.arctan2(yf-bal1[1],xf-bal1[0])
            #print(angle1*360/2/pi)
            angle2 = np.arctan2(yf-balises_reelles[1,0],xf-balises_reelles[0,0])
            #print(angle2*360/2/pi)
            angle = angle2 - angle1
        
        else :
            b =np.sqrt((abs(bal1[1])-abs(bal2[1]))**2+(abs(bal1[0])-abs(bal2[0]))**2)
            al_kashi = np.arccos(max((d2**2+b**2-d1**2)/(2*d2*b),-1))
            xf = -d2*np.cos(al_kashi)+balises_reelles[0,1]
            yf = d2*np.sin(al_kashi)+balises_reelles[1,1]
            angle1 = np.arctan2(yf-bal2[1],xf-bal2[0])
            angle2 = np.arctan2(yf-balises_reelles[1,1],xf-balises_reelles[0,1])
            angle = angle2 - angle1
    
    else : 
        b =np.sqrt((abs(bal3[1])-abs(bal4[1]))**2+(abs(bal3[0])-abs(bal4[0]))**2)
        al_kashi = np.arccos((d4**2+b**2-d3**2)/(2*d4*b))
        xf = d4*np.sin(al_kashi)+balises_reelles[0,3]-100
        yf = -d4*np.cos(al_kashi)+balises_reelles[1,3]
    
    return(xf,yf,angle)
    
def main(lidar,x,y,cap):
    #print('cap',cap)
    balises_reelles = np.array([[100,1900,-60,1000],[-30,-30,1500,3020]])   #Positions exactes dans le repère
    xrob = 0  #Position initiale du robot
    yrob = 0
    theta = cap + 0.52
    zones_rech = balises_reelles.copy()  #Positions des balises par rapport au robot = zones de recherches
 
    
    zones_rech,depx,depy = dep_zones(x,y,theta,zones_rech) # Mise à jour des zones de recherches
    #print("zones de recherche :",zones_rech)
    bal1,bal2,bal3,bal4 = repere(lidar,zones_rech,depx,depy,theta)
    xf, yf, angle = local(x,y,bal1,bal2,bal3,bal4)
    #print(xf,yf)
    #print((cap+angle)*360/2/np.pi)
    return (xf,yf,cap+angle+np.pi/2)


if __name__ =="__main__":
    
    print("debut")
    lidar = connect('/dev/ttyUSB0')
    disconnect(lidar)
    lidar = connect('/dev/ttyUSB0')
    print(main(lidar,255,295,-np.pi/2))
    disconnect(lidar)
    
