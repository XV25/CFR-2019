from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import serial


class lidar():

    def __init__(self,addr):
        
        
        self.addr= addr
        self.xrob = 520 #position initiale du robot
        self.yrob = 160
        self.balises_reelles = np.array([[100,1900,-60,1000],[-30,-30,1500,3020]]) #position exactes dans le repère
        self.r = 150 #rayon de recherche

    
    def connect(self):
        lidar = RPLidar(self.addr) # demarre le lidar
        info = lidar.get_info()
        print(info)
        health = lidar.get_health()
        print(health)

    def disconnect(self):
        lidar = RPLidar(self.addr)
        lidar.stop()  # stop le lidar
        lidar.stop_motor()
        lidar.disconnect()

    def dep_zones(self,x,y,theta,zones):
        zones_f = zones.copy()
        depx = x-self.xrob
        depy = y-self.yrob
        zones_f[0,:] -= depx
        zones_f[1,:] -= depy
        mat = np.array([[np.cos(-theta),-np.sin(-theta)],[np.sin(-theta),np.cos(-theta)]])
        for i in range(len(zones[0])):
            bal = mat@(zones_f[:,i].reshape(2,1)-np.array([[self.xrob],[self.yrob]]))+np.array([[self.xrob],[self.yrob]])
            zones_f[0,i] = bal[0,0]
            zones_f[1,i] = bal[1,0]
        return(zones_f,depx,depy)
    
    def repere(self,balises,depx,depy,theta):
        lidar = RPLidar(self.addr)
        abscisse = []
        ordonnee = []
        x_v = []
        y_v = []
        for i, scan in enumerate(lidar.iter_measurments()):
            valeur = scan[1]
            angle = scan[2]*2*np.pi/360
            x = -scan[3] * np.cos(angle + np.pi/2) + self.xrob
            y = scan[3] * np.sin(angle + np.pi/2) + self.yrob
            x_v.append(x)
            y_v.append(y)
            if valeur == 15 and self.test_zone(x,y,balises):
                abscisse.append(x)
                ordonnee.append(y)
            if i>=500 :
                lidar.stop()
                lidar.disconnect()
                balise1,balise2,balise3,balise4 = self.pos_balises(abscisse,ordonnee,balises,depx,depy,theta)
                return(balise1,balise2,balise3,balise4)


    def pos_balises(self,abscisse,ordonnee,balises,depx,depy,theta):
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
            if self.test_zone(abscisse[i],ordonnee[i],balises[:,0].reshape(2,1)):
                balise_1.append([abscisse[i],ordonnee[i]])
            if self.test_zone(abscisse[i],ordonnee[i],balises[:,1].reshape(2,1)):
                balise_2.append([abscisse[i],ordonnee[i]])
            if self.test_zone(abscisse[i],ordonnee[i],balises[:,2].reshape(2,1)):
                balise_3.append([abscisse[i],ordonnee[i]])
            if self.test_zone(abscisse[i],ordonnee[i],balises[:,3].reshape(2,1)):
                balise_4.append([abscisse[i],ordonnee[i]])
        if balise_1 != []:
            b1[0,0] = np.mean(np.array(balise_1)[:,0])
            b1[1,0] = np.mean(np.array(balise_1)[:,1])
            b1 = mat@(b1-np.array([[self.xrob],[self.yrob]]))+np.array([[self.xrob],[self.yrob]])+np.array([[depx],[depy]])
        if balise_2 != []:
            b2[0,0] = np.mean(np.array(balise_2)[:,0])
            b2[1,0] = np.mean(np.array(balise_2)[:,1])
            b2 = mat@(b2-np.array([[self.xrob],[self.yrob]]))+np.array([[self.xrob],[self.yrob]])+np.array([[depx],[depy]])
        if balise_3 != []:
            b3[0,0] = np.mean(np.array(balise_3)[:,0])
            b3[1,0] = np.mean(np.array(balise_3)[:,1])
            b3 = mat@(b3-np.array([[self.xrob],[self.yrob]]))+np.array([[self.xrob],[self.yrob]])+np.array([[depx],[depy]])
        if balise_4 != []:
            b4[0,0] = np.mean(np.array(balise_4)[:,0])
            b4[1,0] = np.mean(np.array(balise_4)[:,1])
            b4 = mat@(b4-np.array([[self.xrob],[self.yrob]]))+np.array([[self.xrob],[self.yrob]])+np.array([[depx],[depy]])
        return(b1,b2,b3,b4)



    def test_zone(self,x,y,zones):
        flag = False
        for i in range(len(zones[0])):
            dist = np.sqrt((x-zones[0,i])**2+(y-zones[1,i])**2)
            if dist < self.r :
                flag = True
                return(flag)
        return(flag)

    def local(self,x,y,bal1,bal2,bal3,bal4):
        balises_reelles = self.balises_reelles
        d1 = np.sqrt((y-bal1[1])**2+(x-bal1[0])**2)
        d2 = np.sqrt((y-bal2[1])**2+(x-bal2[0])**2)
        d3 = np.sqrt((y-bal3[1])**2+(x-bal3[0])**2)
        d4 = np.sqrt((y-bal4[1])**2+(x-bal4[0])**2)
        if y <= 1500:
            if x <= 950:
                b = np.sqrt((abs(bal1[1])-abs(bal2[1]))**2+(abs(bal1[0])-abs(bal2[0]))**2)
                al_kashi = np.arccos(max((d1**2+b**2-d2**2)/(2*d1*b),-1))
                xf = d1*np.cos(al_kashi)+balises_reelles[0,0]
                yf = d1*np.sin(al_kashi)+balises_reelles[1,0]
            
            else :
                b = np.sqrt((abs(bal1[1])-abs(bal2[1]))**2+(abs(bal1[0])-abs(bal2[0]))**2)
                al_kashi = np.arccos(max((d2**2+b**2-d1**2)/(2*d2*b),-1))
                xf = -d2*np.cos(al_kashi)+balises_reelles[0,1]
                yf = d2*np.sin(al_kashi)+balises_reelles[1,1]
        
        else : 
            b =np.sqrt((abs(bal3[1])-abs(bal4[1]))**2+(abs(bal3[0])-abs(bal4[0]))**2)
            al_kashi = np.arccos((d4**2+b**2-d3**2)/(2*d4*b))
            xf = d4*np.sin(al_kashi)+balises_reelles[0,3]-100
            yf = -d4*np.cos(al_kashi)+balises_reelles[1,3]
        return(xf,yf)

    def getPose(self,x,y,theta):
        zones_rech = self.balises_reelles.copy()  #Positions des balises par rapport au robot = zones de recherches
        zones_rech,depx,depy = self.dep_zones(x,y,theta,zones_rech) # Mise à jour des zones de recherches
        bal1,bal2,bal3,bal4 = self.repere(zones_rech,depx,depy,theta)
        xf, yf = self.local(x,y,bal1,bal2,bal3,bal4)
        
        print(xf,yf)

if __name__ =="__main__":

    Lid = lidar('COM18')
    Lid.connect()
    Lid.getPose(500,750,0)
    Lid.disconnect()


