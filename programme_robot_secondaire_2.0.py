# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 08:59:15 2019
@author: Bertrand-predator
"""
from __future__ import division
# import matplotlib.pyplot as plt
import numpy as np
# import sys
import serial
import time
from threading import Thread, RLock
import cv2
import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera

##Variables à définir
# port='',

port_moteur = '/dev/ttyACM1'  # 2 '/dev/ttyACM0'
port_mega = '/dev/ttyACM0'  # 3 '/dev/ttyACM1'
distance_minimale = 150  # distance de détection des ultrasons en mm

##Les différents états
global nb_etat
nb_etat = 7  # nombre à modifier
global IDLE, RECHERCHE, TRACKING, CATCH, GO_HOME, EVITEMENT, LARGUAGE
IDLE = 0
RECHERCHE = 1
TRACKING = 2
CATCH = 3
GO_HOME = 4
EVITEMENT = 5
LARGUAGE = 6

rouge, vert, bleu = 0, 1, 2

##variables

# variable pour la camera
global nouvelle_photo
global resultat_photo

nouvelle_photo = False  # True: une nouvelle photo vient d'être traité
resultat_photo = 0  # résultat du traitement d'image pour le tracking

global verrou
verrou = RLock()

robot = None


##class
class PiVideoStream:
    def __init__(self, resolution=(320, 240), framerate=32):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)
        self.frame = None
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        for f in self.stream:
            self.frame = f.array
            self.rawCapture.truncate(0)
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True

class Camera(Thread):

    def __init(self):
        Thread.__init__(self)

    def run(self):
        self.vs = PiVideoStream().start()
        time.sleep(1.0)
        while True:
            frame = self.vs.read()

            # diminution de la résolution du frame
            frame = imutils.resize(frame, width=400)

            cv2.imshow('frame', frame)
            # frameBGR = cv2.GaussianBlur(frame, (5, 5), 0) #on s'en fou de flouter

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            v = cv2.extractChannel(hsv, 0)
            mask = cv2.inRange(v, 170, 179)  # red
            # mask = cv2.inRange(v,55,70) # green
            # mask = cv2.inRange(v,90,100) # blue

            kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
            kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))

            mask_m = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open, iterations=3)
            mask_m = cv2.morphologyEx(mask_m, cv2.MORPH_CLOSE, kernel_close, iterations=3)

            ref, contours, hierachy = cv2.findContours(mask_m, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            galet_position = [0., 0.]
            galet_found = False

            list_center = []
            for c in contours:
                # calculate moments for each contour
                M = cv2.moments(c)

                # calculate x,y coordinate of center
                if (M["m00"] > 300): #filtrage, diminuer le 300 si nécessaire
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    list_center.append([cY, cX])

            if len(list_center) > 0:
                galet_found = True
                list_center_np = np.array(list_center)

                index_max = np.argmax(list_center_np, axis=0)
                position_max = list_center_np[index_max[0]]

                center_image_X = mask_m.shape[1] / 2
                galet_error_X = position_max[1] - center_image_X

                with verrou:
                    global nouvelle_photo, resultat_photo
                    resultat_photo = galet_error_X
                    nouvelle_photo = True
                    print(nouvelle_photo)
                print("palet trouvé")

            else:
                with verrou:
                    global nouvelle_photo
                    nouvelle_photo = False
                    print(nouvelle_photo)
                global robot
                robot.arreter()
                print("aucun palet trouvé")

            time.sleep(0.01)
        cv2.destroyAllWindows()
        vs.stop()

class Robot(Thread):

    def __init__(self):
        Thread.__init__(self)

        # configure the serial connections (the parameters differs on the device you are connecting to)
        # Initialisation connection série avec les cartes arduino, port à changer
        self.ser_moteur = serial.Serial(port=port_moteur, baudrate=9600)
        self.ser_mega = serial.Serial(port=port_mega, baudrate=9600)

        # initialisation des variables
        #
        self.couleur = []
        self.last_couleur = None

        self.etat = IDLE
        self.etat_dernier = 0

        self.action = ''
        self.lastAction = ''

        print("fin de l'initialisation")

    def run(self):
        with verrou:
            global nouvelle_photo, resultat_photo
        print("flag 1")
        time.sleep(3)
        print("flag 2")

        robot.changer_etat(IDLE)

        while True:  # loop()
            if robot.getState() == IDLE:
                '''
                on attend l'ordre de commencer
                '''
                robot.arreter()
                time.sleep(1e-3)

                robot.changer_etat(RECHERCHE)  # provisoire

            elif robot.getState() == RECHERCHE:
                '''
                phase statique, on attend d'avoir trouvé un palet pour démarrer
                '''

                with verrou:
                    if (nouvelle_photo == True):
                        robot.changer_etat(TRACKING)  # provisoire
                time.sleep(0.01)

            elif robot.getState() == TRACKING:
                '''
                On se dirige vers le palet
                '''
                with verrou:
                    if (nouvelle_photo):
                        print("Tracking")
                        print(resultat_photo)
                        if (resultat_photo > 5):
                            robot.deplacer_droite()
                        elif (resultat_photo < -5):
                            robot.deplacer_gauche()
                        else:
                            robot.avancer()
                        nouvelle_photo = False

                time.sleep(1e-3)

            elif robot.getState() == CATCH:
                '''
                Le palet est hors de portée de la caméra, on avance un peu dans l'espoir de le récuperer
                '''
                robot.avancer(100)

            elif robot.getState() == GO_HOME:
                '''
                On a recupéré le palet, on rentre à la maison
                '''
                robot.tourner_gauche()


            elif robot.getState() == LARGUAGE:
                # si on a detecter qu'un seul palet on laisse ouvert suffisamment longtemps pour en déposer hypothétiquement é de la même couleur
                # si on en detecte é de couleurs différentes alors on ouvre la herse uniquement le temps pour qu'un seul sorte (avancer de 7cm)
                pass

            elif robot.getState() == EVITEMENT:
                pass

    def recuperer_couleur(self):
        a, b, c, d, e, f = 95, 140, 180, 220, 300, 350

        self.ser_mega.write('c')  # demande d'envoie des couleurs

        rgb = ''
        while rgb == '':
            rgb = self.ser_mega.readline()

        div = 255

        l = rgb[:-2].decode("utf-8").split(" ")
        r = min(eval(l[0]) / div, 1)
        g = min(eval(l[1]) / div, 1)
        b = min(eval(l[2]) / div, 1)

        ma = max(r, g, b)
        mi = min(r, g, b)

        if (ma == mi):
            t = 0
        elif (ma == r):
            t = (60 * (g - b) / (ma - mi) + 360) % 360
        elif (ma == g):
            t = (60 * (b - r) / (ma - mi) + 120)
        elif (ma == b):
            t = (60 * (r - g) / (ma - mi) + 240)

        if a < t and t < b:  # Vert = 1
            if self.last_couleur != 1:
                self.couleur.append(1)
            self.last_couleur = 1
        elif c < t and t < d:
            if self.last_couleur != 0:  # ROUGE = 0
                self.couleur.append(0)
            self.last_couleur = 0
        elif e < t and t < f:  # Bleu = 2
            if self.last_couleur != 2:
                self.couleur.append(2)
            self.last_couleur = 2
        else:
            self.last_couleur = None

    def recuperer_ultrason(self):
        '''
        Demande à l'Arduino l'état des ultra sons
        '''
        self.ser_mega.write('u')  # demande d'envoie des infos ultrasons

        distances = ''
        while distances == '':
            distances = self.ser_mega.readline()
        l = distances[:-2].decode("utf-8").split(" ")

        return self.traiter_ultrason(l)

    def traiter_ultrason(self, l):
        '''
        renvoie False si il n'y a pas d'obstales, sinon 1 si il est à gauche, 2 si il est au milieu, 3 si il est à droite
        '''
        for i in range(len(l)):
            if l[i] == 0:
                l[i] = 1000
            elif l[i] <= distance_minimale:
                self.changer_etat(EVITEMENT)

        d_d = l[2]  # distance à droite
        d_g = l[0]  # distance à gauche
        d_m = l[1]  # distance à milieu

    def commander_herse(self):
        self.ser_mega.write('h')

    def changer_etat(self, nouvel_etat=None):
        self.etat_dernier = self.etat
        if (nouvel_etat == None):
            self.etat = self.etat + 1
        else:
            self.etat = nouvel_etat

        if self.etat >= nb_etat:
            self.etat = 0
        print("on change d'etat")
        print(self.etat)

        # truc à faire pendant le changement d'état
        if (self.etat_dernier == RECHERCHE and self.etat == TRACKING):
            self.action = 'f'
            self.ser_moteur.write('f'.encode("utf-8"))
            print("on avance")

    def getState(self):
        return self.etat

    def arreter(self):
        if (self.lastAction != 'w'):
            print("on s'arrete")
            self.lastAction = self.action
            self.action = 'w'
            self.ser_moteur.write('w'.encode("utf-8"))

    def avancer(self, distance=None):

        if (self.lastAction != 'f'):
            self.ser_moteur.write('f'.encode("utf-8"))
            self.lastAction = self.action
            self.action = 'f'
            print("on avance tout droit")

        if (distance != None):
            self.ser_moteur.write('a'.encode("utf-8"))
            dis = float(self.ser_moteur.readline())
            if (distance <= dis):
                robot.arreter()
                self.ser_moteur.write('o'.encode("utf-8"))
                self.changer_etat(GO_HOME)

    def tourner_droite(self):
        '''
        tourne de 90 degré, centre de rotation : centre du robot
        '''
        pass

    def tourner_gauche(self):
        '''
        tourne de 90 degré, centre de rotation : centre du robot
        '''
        if (self.lastAction != 'l'):
            self.ser_moteur.write('l'.encode("utf-8"))
            self.lastAction = self.action
            self.action = 'l'

    def deplacer_droite(self):
        '''
        avance en tournant legerement à droite
        '''
        if (self.lastAction != 'd'):
            self.ser_moteur.write('d'.encode("utf-8"))
            self.lastAction = self.action
            self.action = 'd'
            print("palet à droite")

    def deplacer_gauche(self):
        '''
        avance en tournant legerement à gauche
        '''
        if (self.lastAction != 'q'):
            self.ser_moteur.write('q'.encode("utf-8"))
            self.lastAction = self.action
            self.action = 'q'
            print("palet à gauche")


##Fonctions

##script


robot = Robot()
camera = Camera()
camera.start()
robot.start()

robot.join()
camera.join()
