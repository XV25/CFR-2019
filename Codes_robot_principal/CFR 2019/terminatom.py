import sys     # pour la gestion des parametres
import serial  # bibliotheque permettant la communication serie
import time
import numpy as np



class terminatom():
    """
    cette classe permet de regrouper toutes les fonctions utilisable par la rasp pour commander les differentes
    composant. Les communication necessaire pour chaque action seront ecrite dans ces fonctions.
    """

    def __init__(self, pos_x=0, pos_y=0, angle = np.pi/2):
        self.ser = serial.Serial('/dev/ttyACM0',9600)  #connection serie avec la carte arduino base roulante
        self.ser2 = serial.Serial('/dev/ttyACM1',9600)
        self.vg =0
        self.vd = 0
        self.x = pos_x
        self.y = pos_y
        self.theta = angle

        
    #rajouter les variable d'etat utile au fire et a mesure



    def testLed(self):
        """
        declenche les fonction testled du programme arduino (pin10) pour tester la connection serie
        Parametres
        ----------
        aucun

        Renvoie
        -------
        Ecrit la lettre s ou z puis sont code ascii, ce qui confirme que la fonction a ete lance dans l'arduino et
        qu'on a bien lu le retour.
        Allume la led 2 fois 2 secondes avec 2 secondes de pauses
        """
        self.ser.write("je suis la")  #declenche la fonction d'allumage sur la arduino
        print(self.ser.readline())
        time.sleep(2)

        self.ser.write("z")   #declenche la fonction pour eteindre la led sur la arduino
        print(self.ser.readline())
        time.sleep(2)

        self.ser.write('s')#declenche la fonction d'allumage sur la arduino
        print(self.ser.readline())
        time.sleep(2)

        self.ser.write('z')
        print(self.ser.readline())

    def nouvellePos(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        
    def Motor(self, vg,vd):
        print(" moteur : ",vg," et ",vd)
        self.vg = vg
        self.vd  = vd
        self.ser.write('m')
        if (abs(vd) > 255) or (abs(vg) > 255):
            print("la vitesse doit etre comprise entre -255 et 255")
        else:
            
            if vg >= 0:
                ldir = chr(0)
                pwm = chr(vg)
            else :
                ldir = chr(1)
                pwm = chr(abs(vg))
            #print(self.ser.readline())
            self.ser.readline()
            self.ser.write(ldir)
            #print(self.ser.readline())
            self.ser.readline()
            self.ser.write(pwm)
            #print(self.ser.readline())
            self.ser.readline()


            if vd >= 0:
                ldir = chr(1)
                pwm = chr(vd)
            else :
                ldir = chr(0)
                pwm = chr(abs(vd))

            self.ser.write(ldir)
            #print(self.ser.readline())
            self.ser.readline()
            self.ser.write(pwm)
            #print(self.ser.readline())
            self.ser.readline()

    
        

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
        odoleft = int(self.ser.readline())
        print(odoleft, odoright)
        return (odoleft,odoright)


    def ultrason(self):
        d = []
        print(" commande ultrason \n")
        self.ser2.write('u')
        print(self.ser2.readline())
        for i in range(8):
            di = self.ser2.readline()
            di = int(di)
            print(di)
            d.append(di)
        
        return d



    def avanceDroit(self,vitesse):
        self.Motor(vitesse,vitesse)
        t0 = time.time()
        while (time.time()-t0 < 2):
            el,er = self.odometer()
            erreur = el-er
            self.Motor(vitesse - int(erreur/2), vitesse + int(erreur/2))
        self.arret()


if __name__ == "__main__":
    rob = terminatom()

    l0,r0 = rob.odometer()
    rob.avanceDroit(180)
    time.sleep(1)
    '''
    for i in range(10):
        time.sleep(1)
        rob.ultrason()
    '''
    rob.arret()
    l1,r1 = rob.odometer()
    print("encodeur : ",l1-l0,",",r1-r0)
##    rob.odometer()
##    time.sleep(2)
##    rob.odometer()

##    rob.ultrason()
