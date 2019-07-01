# -*- coding: utf-8 -*-
"""
Created on Sat May 11 10:58:57 2019

@author: ehnla
"""

"""
Programme permettant la capture des images, puis la détection des palets de couleur.
La détection des couleurs a lieu grâce aux fonctions du fichier detect_auto_global_opti_max_2.
"""

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
from detect_auto_global_opti_max2 import * #nom du fichier dans lequel se trouvent les fonctions pour opencv
import cv2
#from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
import imutils
# module imutils : module avec des classes utiles pour le traitement d'image. Permet notamment 
# d'enregistrer le nombre de FPS pour la capture d'image, mais aussi d'effectuer 
# du multithreading.
# Le multithreading s'effectue via la classe PiVideoSteam (classe redéfinie juste
# en dessous ici).

class PiVideoStream:
    def __init__(self, resolution=(320, 240), framerate=32):
        """
        Initialise la classe pour effectuer du multithreading.
        """
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,format="bgr", use_video_port=True)
        self.frame = None
        self.stopped = False
    
    def start(self):
        """
        Lance la capture d'image via multithreading
        """
        Thread(target=self.update, args=()).start()
        return self
    
    def update(self):
        """
        Met à jour l'image capturée
        """
        for f in self.stream:
            self.frame = f.array
            self.rawCapture.truncate(0)
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return
            
    def read(self):
        """
        Renvoie l'image capturée
        """
        return self.frame
    
    def stop(self):
        """
        Stoppe la capture d'image.
        """
        self.stopped = True



def detect_gold(vs,gd,display = 0,num_frames = 1):
    """
    Programme permettant de détecter le goldenium.
    
    Entrée : 
        vs : Objet PiVideoStream, contenant la prise des images
        gd : indique si le robot se trouve sur le côté gauche ou droit du terrain 
        (par rapport au côté proche de la balance). G = True, D = False 
        display : permet d'afficher ou non le résultat (l'image et la position estimée
        du centre des palets)
        num_frames : indique le nombre d'images à traiter (de façon générale, une seule
        suffit : il n'y a pas de changements entre les images pour une même position 
        du robot).
        
    Sortie : 
        L : Liste contenant la position du centre du palet détecté.
        """
        
    fps = FPS().start()
    while fps._numFrames < num_frames:
    	# grab the frame from the threaded video stream and resize it
    	# to have a maximum width of 400 pixels
    	frame = vs.read()
    	frame = imutils.resize(frame, width=400)
    	#L,Lv,L_s = detect_gold_vid(frame,1,250)
    	L,L_s = detect_gold_vid(frame,gd,display)
    	# check to see if the frame should be displayed to our screen
    	if display > 0:
            cv2.circle(frame,(L[1],0), 4, (0,100,255), -1) # coordonnée en y du palet
            cv2.circle(frame,(0,L[0]), 4, (0,0,255), -1) # coordonnée en x du palet
            cv2.circle(frame,(L[1],L[0]), 4, (0,0,255), -1) # position du palet
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(0) 
	     # update the FPS counter
    	fps.update()
    fps.stop()
    
    return(L)
    

def detect_colors(vs,gd,display = 0,num_frames = 1):
    """
    Programme permettant de détecter les palets rouges, bleus  verts. Il renvoie
    alors la position des palets les plus proches de la balance, pour chaque couleur.
    
    Entrée : 
        vs : Objet PiVideoStream, contenant la prise des images
        gd : indique si le robot se trouve sur le côté gauche ou droit du terrain 
        (par rapport au côté proche de la balance). G = True, D = False 
        display : permet d'afficher ou non le résultat (l'image et la position estimée
        du centre des palets)
        num_frames : indique le nombre d'images à traiter (de façon générale, une seule
        suffit : il n'y a pas de changements entre les images pour une même position 
        du robot).
        
    Sortie : 
        L : Liste contenant la position des palets les plus proches du milieu du robot,
        pour chaque couleur.
        """
        
    fps = FPS().start()
    while fps._numFrames < num_frames:
    	# grab the frame ffrom the threaded video stream and resize it
    	# to have a maximum width of 400 pixels
    	frame = vs.read()
    	frame = imutils.resize(frame, width=400)
    	L,L_s = all_detect_color_vid(frame,gd,display)
    	# check to see if the frame should be displayed to our screen
    	if display > 0:
            col_circ = [(100,0,255),(0,255,100),(255,100,0)]
            for k in range(len(L)):
                col = col_circ[k]
                cv2.circle(frame,(L[k][1],L[k][0]), 4, col, -1) 
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(0) 
	# update the FPS counter
    	fps.update()
    fps.stop()
    return(L)

def detect_color(vs,gd,color,display = 0,num_frames = 1):
    """
    Programme permettant de détecter les palets rouges, bleus ou verts. Il renvoie
    alors la position des palets les plus proches de la balance.
    
    Entrée : 
        vs : Objet PiVideoStream, contenant la prise des images
        gd : indique si le robot se trouve sur le côté gauche ou droit du terrain 
        (par rapport au côté proche de la balance). G = True, D = False 
        color : indique la couleur du palet à détecter.
        display : permet d'afficher ou non le résultat (l'image et la position estimée
        du centre des palets)
        num_frames : indique le nombre d'images à traiter (de façon générale, une seule
        suffit : il n'y a pas de changements entre les images pour une même position 
        du robot).
        
    Sortie : 
        L : Liste contenant la position du palet le plus proche du milieu du robot.
        """

    fps = FPS().start()
    while fps._numFrames < num_frames:
    	# grab the frame ffrom the threaded video stream and resize it
    	# to have a maximum width of 400 pixels
    	frame = vs.read()
    	frame = imutils.resize(frame, width=400)
    	L,L_s = detect_color_vid(frame,color,gd,display)
    	# check to see if the frame should be displayed to our screen
    	if display > 0:
            cv2.circle(frame,(L[1],L[0]), 4, (0,255,255), -1) 
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(0) 
	# update the FPS counter
    	fps.update()
    fps.stop()
    return(L)


if __name__ =="__main__":
    display = 1
    print("[INFO] sampling THREADED frames from `picamera` module...")
    vs = PiVideoStream().start()
    time.sleep(2.0)
    
    detect_gold(vs,0,1,6)
    #detect_color(vs,0,'G',1,6)
    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()
