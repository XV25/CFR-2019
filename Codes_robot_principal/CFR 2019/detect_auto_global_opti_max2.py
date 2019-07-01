## -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 21:24:55 2019

@author: ehnla
"""

""" 
Programmes permettant de reconnaître les centres des palets présents dans les images
données.
"""

# -*- coding: utf-8 -*-

###############################################################################
import numpy as np  # module pour la manipulation de matrice
import time
import time
import picamera
import picamera.array
import cv2 # module pour la manipulation d'image via OpenCV

###############################################################################

def Egalisation_HSL_col(img_BGR):
    """
    Permet de réhausser les contrastes, via l'égalisation des histogrammes
    des composantes de l'image, pour la détection de palets RGB.
    A noter : pour du HSL, l'égalisation n'a généralement lieu que sur la
    composante L (luminance), parfois sur la composante S, jamais sur la H 
    (forte dégradation des couleurs de l'image sinon).
    """
    img_HSL = cv2.cvtColor(img_BGR,cv2.COLOR_BGR2HLS) # Image BGR --> HSV
    h,l,s   = cv2.split(img_HSL)                      # Extraction des 3 plans HSV notamment value v
    h_egal = cv2.equalizeHist(h)
    s_egal  = cv2.equalizeHist(s)                     # Egalisation histogramme sur s
    l_egal  = cv2.equalizeHist(l)                     # Egalisation histogramme sur v
    
    img_egal= img_HSL.copy()               # Copie de l'image HSL
    #img_egal[:,:,0] = h_egal             # Modification du plan h
    #img_egal[:,:,2] = s_egal             # Modification du plan s
    #img_egal[:,:,1] = l_egal              # Modification du plan l (parfois utile pour détection du blanc)
    
    return img_result


def Egalisation_HSL_gold(img_BGR):
    """
    Permet de réhausser les contrastes, via l'égalisation des histogrammes
    des composantes de l'image, pour la détection du goldenium.
    A noter : pour du HSL, l'égalisation n'a généralement lieu que sur la
    composante L (luminance), parfois sur la composante S, jamais sur la H 
    (forte dégradation des couleurs de l'image sinon).
    """
    img_HSL = cv2.cvtColor(img_BGR,cv2.COLOR_BGR2HLS) # Image BGR --> HSL
    h,l,s   = cv2.split(img_HSL)                      # Extraction des 3 plans HSL notamment value L
    h_egal = cv2.equalizeHist(h)
    s_egal  = cv2.equalizeHist(s)                     # Egalisation histogramme sur s
    l_egal  = cv2.equalizeHist(l)                     # Egalisation histogramme sur v
    
    img_egal= img_HSL.copy()               # Copie de l'image HSV
    #img_egal[:,:,0] = h_egal             # Modification du plan h
    #img_egal[:,:,2] = s_egal             # Modification du plan s
    img_egal[:,:,1] = l_egal              # Modification du plan l (parfois utile pour détection du blanc)
    
    return img_egal




def detect_gold_vid(image,gd,display = 0,ydist = 250,ech = 1,resx = 0,resy = 0,L = [],avan_y = 0): 
    """
    Programme permettant de détecter le goldenium présent sur les images.
    Renvoie la position (0,0) si le goldenium n'est pas détecté sur l'image.
    Pour cela, les étapes sont les suivantes : 
        -égalisation des histogrammes des composants R,G et B de l'image.
        -filtrage de l'image selon les composants max / min notées dans l'algorithme
        (issues d'un calibrage)
        - création et application des filtres d'ouverture et de fermeture
        -calcul du périmètres des objets restants sur l'image, sélection de l'objet
        dont le périmètre possède la même taille que celui du palet.
        -renvoi de la position de l'objet.
    
    Entrée :
        image : image traitée par le programme.
        gd : indique si le robot se trouve sur le côté gauche ou droit du terrain 
        (par rapport au côté proche de la balance). G = True, D = False 
        display : permet d'afficher ou non le résultat (l'image et la position estimée
        du centre des palets)
        
        Optionnel : variable donnant une approximation de la distance palet / caméra,
        afin d'ajuster la sélection du périmètre à détecter (non installé) : 
            ydist : distance palet / caméra.
        
        Optionnel : variables permettant de réduire la zone de détection du goldenium,
        afin de réduire le temps de détection entre plusieurs détections successives 
        (Efficacité limitée en pratique : il est plus efficace de prendre dès le début
        une image de faible résolution. De plus, la fonction ne semble pas fonctionner
        parfaitement actuellement) :
            ech : degré d'échantillonage : définit de combien la résolution doit être diminuée.
            resx : résolution en x de l'image précédente.
            resy : résolution en y de l'image précédente.
            L : liste contenant la position du centre dans l'image précédente.
            ayan_y : déplacement du robot en y entre les deux images.
            
    Sortie : 
        [cy,cx] : position du centre du palet détecté.
        [height,width] : taille de l'image         
                                                                      ----> y
    Rappel  :  Axe x : va de haut à gauche à bas à gauche            |
               Axe y : va de haut à gauche à haut à droite           v x
    
    """

    # Etape 0 : réduction de l'image autour du dernier point de détection
    # du palet (si conditions respectées)
    if L != [] and (L[0] !=0 and L[1] != 0):
        cx = L[0]
        cy = L[1]
        s_sel = min(resx,resy)
        mx = max(int(cx-s_sel),0)
        Mx = min(int(cx+s_sel),resx)
        my = max(int(cy-s_sel-avan_y),0)
        My = min(int(cy+s_sel-avan_y),resy)
        #print(mx,Mx,my,My,s_sel)

        img_L = image[mx:Mx,my:My,::] 
        img_C = img_L[::ech,::ech,::]
    else : 
        img_C  = image[::ech,::ech,::]    
    t0 = time.time()
    #print("shape : ", img_C.shape)
    
    #Etape 1 : égalisation  HSL

    imgHSL= Egalisation_HSL_gold(img_C)
    
    t1 = time.time()
    #print("Tps ega : ",t1 -t0 )

    # Etape 2 : filtrage des composantes
    # Init des seuils H,S,L max et min, ainsi que de la taille des filtres
    # d'ouverture et de fermeture (devant être impairs)

    Hmin =50
    Hmax = 255
    Smin =0
    Smax = 255 
    Lmin = 160 
    Lmax = 255
    k1 =2 
    kf = 2*k1 + 1 
    k2 =2
    ko = 2*k2 + 1 
 
    lower = np.array([Hmin,Lmin,Smin])
    upper = np.array([Hmax,Lmax,Smax])
    img_bin = cv2.inRange(imgHSL,lower,upper)

    t2 = time.time()
    #print("Tps filtrage : ", t2-t1)
    
    
    # Etape 3 : Application des filtres d'ouvertures et de fermeture, uniquement
    # si ceux-ci sont activés 
    if k1 == -1 or k2 == -1:
        if display > 0:
            cv2.imshow('Ap opening',img_bin)
        contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #[1:]
    else :
        kernelf = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kf, kf))
        kernelo = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ko, ko))
        et1 = cv2.morphologyEx(img_bin, cv2.MORPH_CLOSE, kernelf)
        et2 = cv2.morphologyEx(et1, cv2.MORPH_OPEN, kernelo)
        if display > 0:
            cv2.imshow('Ap opening',et2)
        contours, hierarchy = cv2.findContours(et2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #[1:]

    t3 = time.time()
    
    #print("Tps ouverture / fermeture : ", t3 -t2)

    #Etape 4 : sélection du périmètre 
    
    cx,cy = 0,0
    T = 0
    v_seuil = 9500/(ech**2) #(4**ech)#50000/(ech*ydist)
    #print(v_seuil)
    for i in range (len(contours)):
        cnt = contours[i]
        M = cv2.moments(cnt)
        if M['m00'] > v_seuil : #and M['m00']< 3*v_seuil : 
            cx = int(M['m10']/(M['m00']+1*10**-5))
            cy = int(M['m01']/(M['m00']+1*10**-5))
            #print(M['m00']) 
            T += 1 
            if T > 1 :
                break
    height,width = img_C.shape[0:2]
    #print(height,width)
    return([cy,cx],[height,width])


def detect_color_vid(image,color,gd,display = 0,ydist =250,ech = 1,resx = 0,resy = 0,L = [],avan_y = 0): 
    """
    Programme permettant de détecter le palet de la couleur donnée en entrée sur 
    les images.
    Renvoie la position (0,0) si le palet n'est pas détecté sur l'image.
    Pour cela, les étapes sont les suivantes : 
        -égalisation des histogrammes des composants R,G et B de l'image.
        -filtrage de l'image selon les composants max / min notées dans l'algorithme
        (issues d'un calibrage)
        - création et application des filtres d'ouverture et de fermeture
        -calcul du périmètres des objets restants sur l'image, sélection de l'objet
        dont le périmètre possède la même taille que celui du palet.
        -sélection de l'objet le plus proche de la balance
        -renvoi de la position de l'objet.
    
    Entrée :
        image : image traitée par le programme.
        gd : indique si le robot se trouve sur le côté gauche ou droit du terrain 
        (par rapport au côté proche de la balance). G = True, D = False 
        display : permet d'afficher ou non le résultat (l'image et la position estimée
        du centre des palets)
        
        Optionnel : variable donnant une approximation de la distance palet / caméra,
        afin d'ajuster la sélection du périmètre à détecter (non installé) : 
            ydist : distance palet / caméra.
        
        Optionnel : variables permettant de réduire la zone de détection du goldenium,
        afin de réduire le temps de détection entre plusieurs détections successives 
        (Efficacité limitée en pratique : il est plus efficace de prendre dès le début
        une image de faible résolution. De plus, la fonction ne semble pas encore fonctionner
        parfaitement actuellement) :
            ech : degré d'échantillonage : définit de combien la résolution doit être diminuée.
            resx : résolution en x de l'image précédente.
            resy : résolution en y de l'image précédente.
            L : liste contenant la position du centre dans l'image précédente.
            ayan_y : déplacement du robot en y entre les deux images.
            
    Sortie : 
        [cy,cx] : position du centre du palet détecté.
        [height,width] : taille de l'image         
                                                                      ----> y
    Rappel  :  Axe x : va de haut à gauche à bas à gauche            |
               Axe y : va de haut à gauche à haut à droite           v x
    
    """


    # Etape 0 : réduction de l'image autour du dernier point de détection
    # du palet (si conditions respectées)
    if L != [] or (L[0] !=0 and L[1] != 0):
        cx = L[0]
        cy = L[1]
        s_sel = min(resx,resy)
        mx = max(int(cx-s_sel),0)
        Mx = min(int(cx+s_sel),resx)
        my = max(int(cy-s_sel-avan_y),0)
        My = min(int(cy+s_sel-avan_y),resy)
        #print(mx,Mx,my,My,s_sel)

        img_L = image[mx:Mx,my:My,::] 
        img_C = img_L[::ech,::ech,::]
    else : 
        img_C  = image[::ech,::ech,::]    
    t0 = time.time()
    #print("shape : ", img_C.shape)
    
    #Etape 1 : égalisation  HSL
    # inutile dans les tests effectués pour le moment; on effectue juste la conversion en HSL

    #imgHSL = Egalisation_HSL_col(img_C)
    imgHSL = cv2.cvtColor(img_C,cv2.COLOR_BGR2HLS)

    # Etape 2 : filtrage des composantes
    # Init des seuils H,S,L max et min, ainsi que de la taille des filtres
    # d'ouverture et de fermeture (devant être impairs)

    if color == "G":
        Hmin = 30
        Hmax = 90
        Smin = 15#45#105
        Smax = 255
        Lmin = 0#33
        Lmax = 200 #121#255
        k1 =1
        kf = 2*k1 + 1 
        k2 =1
        ko = 2*k2 + 1 
    
    elif color == "R":
        Hmin = 163 #105
        Hmax = 255
        Smin = 50 #97#27
        Smax = 255
        Lmin = 0 #73
        Lmax = 255#114#250
        k1 =2
        kf = 2*k1 + 1 
        k2 =1
        ko = 2*k2 + 1 


    elif color == "B":
        Hmin = 100#50 
        Hmax = 140#255#157
        Smin  = 160#53
        Smax = 255
        Lmin = 40
        Lmax = 200#170#250
        k1 =1
        kf = 2*k1 + 1 
        k2 =1
        ko = 2*k2 + 1 
    
    lower = np.array([Hmin,Lmin,Smin])
    upper = np.array([Hmax,Lmax,Smax])
        
    img_bin = cv2.inRange(imgHSL,lower,upper)

    # Etape 3 : Application des filtres d'ouvertures et de fermeture, uniquement
    # si ceux-ci sont activés 
    
    if k1 == -1:
        if display > 0:
            cv2.imshow('Ap opening',img_bin)
        contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #[1:]
    else :
        kernelf = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kf, kf))
        kernelo = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ko, ko))
        et1 = cv2.morphologyEx(img_bin, cv2.MORPH_CLOSE, kernelf)
        et2 = cv2.morphologyEx(et1, cv2.MORPH_OPEN, kernelo)
        if display > 0:
            cv2.imshow('Ap opening',et2)
        contours, hierarchy = cv2.findContours(et2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #[1:]

    # Etape 4 : sélection du périmètre
    # Actuellement, un seul palet est sélectionné : modifier T > [nombre de palets détectés]
    # pour en détecter plusieurs.
    
    T = 0
    L = []
    cx,cy = 0,0
    for i in range (len(contours)):
        cnt = contours[i]
        M = cv2.moments(cnt)
        if (M['m00'] > 3000) :
            cx = int(M['m10']/(M['m00']+1*10**-5))
            cy = int(M['m01']/(M['m00']+1*10**-5))
            L.append([cx,cy])
            #print(M['m00'])

            T += 1
            if T > 1 :
                #print(T)
                break

    #print("Tps exécution : ", time.time() - t0)

    # Etape 5 : sélection de l'objet le plus proche de la balance  
    height,width = img_C.shape[0:2]
    if gd == True :
        """Côté gauche du terrain """
        pos_s_x = height/2
        pos_s_y = 0
    else:
        """Côté droit du terrain """
        pos_s_x = height/2
        pos_s_y = width
        
    mx,my = 100000,100000
    for k in range(len(L)):
        if abs(L[k][0] -pos_s_x) < mx and abs(L[k][1] - pos_s_y) < my:
            mx = L[k][0]-pos_s_x
            my  = L[k][1] - pos_s_y
            cx = L[k][0]
            cy = L[k][1]

    return([cy,cx],[height,width])

def all_detect_color_vid(image,gd,display = 0,ydist = 250,ech = 1,resx = 0,resy = 0,L = [],avan_y = 0): 
    """
    Programme permettant de détecter les palets RGB présents sur l'image.
    Renvoie les palets les plus proches de la balance.
    Renvoie la position (0,0) si le palet n'est pas détecté sur l'image.
    Pour cela, les étapes sont les suivantes : 
        -égalisation des histogrammes des composants R,G et B de l'image.
        -filtrage de l'image selon les composants max / min notées dans l'algorithme
        (issues d'un calibrage)
        - création et application des filtres d'ouverture et de fermeture
        -calcul du périmètres des objets restants sur l'image, sélection de l'objet
        dont le périmètre possède la même taille que celui du palet.
        -sélection de l'objet le plus proche de la balance
        -renvoi de la position de l'objet.
    
    Entrée :
        image : image traitée par le programme.
        gd : indique si le robot se trouve sur le côté gauche ou droit du terrain 
        (par rapport au côté proche de la balance). G = True, D = False 
        display : permet d'afficher ou non le résultat (l'image et la position estimée
        du centre des palets)
        
        Optionnel : variable donnant une approximation de la distance palet / caméra,
        afin d'ajuster la sélection du périmètre à détecter (non installé) : 
            ydist : distance palet / caméra.
        
        Optionnel : variables permettant de réduire la zone de détection du goldenium,
        afin de réduire le temps de détection entre plusieurs détections successives 
        (Efficacité limitée en pratique : il est plus efficace de prendre dès le début
        une image de faible résolution. De plus, la fonction ne semble pas encore fonctionner
        parfaitement actuellement) :
            ech : degré d'échantillonage : définit de combien la résolution doit être diminuée.
            resx : résolution en x de l'image précédente.
            resy : résolution en y de l'image précédente.
            L : liste contenant la position du centre dans l'image précédente.
            ayan_y : déplacement du robot en y entre les deux images.
            
    Sortie : 
        L_all : liste contenant les position des centres des palets RGB les
        plus proches de la balance (bords de l'image)
        [height,width] : taille de l'image         
                                                                      ----> y
    Rappel  :  Axe x : va de haut à gauche à bas à gauche            |
               Axe y : va de haut à gauche à haut à droite           v x
    
    """
    
   # Etape 0 : réduction de l'image autour du dernier point de détection
    # du palet (si conditions respectées)
    if L != [] or (L[0] !=0 and L[1] != 0):
        cx = L[0]
        cy = L[1]
        s_sel = min(resx,resy)
        mx = max(int(cx-s_sel),0)
        Mx = min(int(cx+s_sel),resx)
        my = max(int(cy-s_sel-avan_y),0)
        My = min(int(cy+s_sel-avan_y),resy)
        #print(mx,Mx,my,My,s_sel)

        img_L = image[mx:Mx,my:My,::] 
        img_C = img_L[::ech,::ech,::]
    else : 
        img_C  = image[::ech,::ech,::]    
    t0 = time.time()
    #print("shape : ", img_C.shape)
    
    #Etape 1 : égalisation  HSL
    # inutile dans les tests effectués pour le moment; on effectue juste la conversion en HSL

    #imgHSL = Egalisation_HSL_col(img_C)
    imgHSL = cv2.cvtColor(img_C,cv2.COLOR_BGR2HLS)
    
    all_col = ['R','G','B']
    col_circ = [(100,0,255),(0,255,100),(255,100,0)]
    L_all = []
    
    # Réalisation des étapes 2,3,4 et 5 pour chaque couleur.
    
    for i in range(3):
        # Etape 2 : filtrage des composantes
        # Init des seuils H,S,L max et min, ainsi que de la taille des filtres
         # d'ouverture et de fermeture (devant être impairs)
        
        color = all_col[i]
        col = col_circ[i]
        if color == "G":
            Hmin = 30
            Hmax = 90
            Smin = 15#45#105
            Smax = 255
            Lmin = 0#33
            Lmax = 200 #121#255
            k1 =1
            kf = 2*k1 + 1 
            k2 =1
            ko = 2*k2 + 1 
        
        elif color == "R":
            Hmin = 163 #105
            Hmax = 255
            Smin = 50 #97#27
            Smax = 255
            Lmin = 0 #73
            Lmax = 255#114#250
            k1 =2
            kf = 2*k1 + 1 
            k2 =1
            ko = 2*k2 + 1 


        elif color == "B":
            Hmin = 90#50
            Hmax = 157
            Smin  = 100#53
            Smax = 255
            Lmin = 40
            Lmax = 150#250
            k1 =1
            kf = 2*k1 + 1 
            k2 =1
            ko = 2*k2 + 1 
        
        lower = np.array([Hmin,Lmin,Smin])
        upper = np.array([Hmax,Lmax,Smax])
            
        img_bin = cv2.inRange(imgHSL,lower,upper)

   # Etape 3 : Application des filtres d'ouvertures et de fermeture, uniquement
    # si ceux-ci sont activés 
    
        if k1 == -1:
            if display > 0:
                cv2.imshow('Ap opening',img_bin)
            contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #[1:]
        else :
            kernelf = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kf, kf))
            kernelo = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ko, ko))
            et1 = cv2.morphologyEx(img_bin, cv2.MORPH_CLOSE, kernelf)
            et2 = cv2.morphologyEx(et1, cv2.MORPH_OPEN, kernelo)
            if display > 0:
                cv2.imshow('Ap opening',et2)
            contours, hierarchy = cv2.findContours(et2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #[1:]

    # Etape 4 : sélection du périmètre
    # Actuellement, un seul palet est sélectionné : modifier T > [nombre de palets détectés]
    # pour en détecter plusieurs.

        T = 0
        L = []
        cx,cy = 0,0
        for i in range (len(contours)):
            cnt = contours[i]
            M = cv2.moments(cnt)
            if M['m00'] > 4500 and M['m00']<10000:
                cx = int(M['m10']/(M['m00']+1*10**-5))
                cy = int(M['m01']/(M['m00']+1*10**-5))
                L.append([cx,cy])
                #print(M['m00'])
                T += 1
                if T > 1 :
                    break

        #print("Tps exécution : ", time.time() - t0)

        height,width = img_C.shape[0:2]
        if gd == True :
            """Côté gauche du terrain """
            pos_s_x = height/2
            pos_s_y = 0
        else:
            """Côté droit du terrain """
            pos_s_x = height/2
            pos_s_y = width

        # Etape 5 : sélection, parmi les palets sélectionnées, de ceux les
        # plus proches du bord de l'image.

        mx,my = 100000,100000
        for k in range(len(L)):
            if abs(L[k][0] -pos_s_x) < mx and abs(L[k][1] - pos_s_y) < my:
                mx = L[k][0]-pos_s_x
                my  = L[k][1] - pos_s_y
                cx = L[k][0]
                cy = L[k][1]
        L_all.append([cy,cx])
    
    # Toutes les couleurs ont été traitées, renvoi du résultat
    return(L_all,[height,width])


if __name__ == "__main__":
    
    with picamera.PiCamera(resolution = (900,600)) as camera:
        #camera.start_preview()
        time.sleep(2)
        with picamera.array.PiRGBArray(camera) as stream :
            k = 0
            camera.capture(stream, format = 'bgr')
            image = stream.array
            L,Lv,L_s = detect_gold_vid(image,2,250)
            stream.truncate(0)
            while (k < 10):
                camera.capture(stream, format = 'bgr')
                image = stream.array
                L,Lv,L_s = detect_gold_vid(image,1,250,L_s[0],L_s[1],L,0)
                cv2.waitKey(1) & 0xFF                   
                cv2.destroyAllWindows()
                stream.truncate(0)
                k +=1
			
