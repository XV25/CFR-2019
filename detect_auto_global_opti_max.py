## -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 21:24:55 2019

@author: ehnla
"""
# code rgb:
#Rouge : 230,0,0
#Vert : 77,255,25
#Bleu : 25,153,255

# -*- coding: utf-8 -*-

###############################################################################
import numpy as np  # module pour la manipulation de matrice
import time
#import Threading
#import pylab as plt # module pour affichage des données
#from matplotlib import pyplot as plt    # Module image propre à python 
#from scipy.ndimage import label, generate_binary_structure

import cv2          # module pour la manipulation d'image via OpenCV

###############################################################################

def Egalisation_HSL_col(img_BGR):
    img_HSL = cv2.cvtColor(img_BGR,cv2.COLOR_BGR2HLS) # Image BGR --> HSV
    h,l,s   = cv2.split(img_HSL)                      # Extraction des 3 plans HSV notamment value v
    h_egal = cv2.equalizeHist(h)
    s_egal  = cv2.equalizeHist(s)                     # Egalisation histogramme sur s
    l_egal  = cv2.equalizeHist(l)                     # Egalisation histogramme sur v
    
    img_egal= img_HSL.copy()                          # Copie de l'image HSV
   # img_egal[:,:,0] = h_egal
   # img_egal[:,:,2] = s_egal                          # Modification du plan s
  #  img_egal[:,:,1] = l_egal                          # Modification du plan v
    
    # Uniquement sur L, pt sur S, pas sur H
    img_result      = cv2.cvtColor(img_egal,cv2.COLOR_HLS2BGR) # Image HSV --> BGR 
    
    return img_result


def Egalisation_HSL_gold(img_BGR):
    img_HSL = cv2.cvtColor(img_BGR,cv2.COLOR_BGR2HLS) # Image BGR --> HSV
    h,l,s   = cv2.split(img_HSL)                      # Extraction des 3 plans HSV notamment value v
    #h_egal = cv2.equalizeHist(h)
#    s_egal  = cv2.equalizeHist(s)                     # Egalisation histogramme sur s
    l_egal  = cv2.equalizeHist(l)                     # Egalisation histogramme sur v
    
    img_egal= img_HSL.copy()                          # Copie de l'image HSV
    #img_egal[:,:,0] = h_egal
   # img_egal[:,:,2] = s_egal                          # Modification du plan s
    img_egal[:,:,1] = l_egal                          # Modification du plan v
    
    
    # Uniquement sur L, pt sur S, pas sur H

    return img_egal



def detect_gold(fname,ech,ydist,resx = 0,resy = 0,L = [],avan_y = 0): 
    # Axe x : de haut à gche à bas à gauche
    # Axe y : de haut à gche à haut à dte
    # ech : degré d'échantillonage
    if L != []:
        cx = L[0]
        cy = L[1]
        s_sel = min(resx,resy)/2
        mx = max(int(cx-s_sel),0)
        Mx = min(int(cx+s_sel),resx)
        my = max(int(cy-s_sel-avan_y),0)
        My = min(int(cy+s_sel-avan_y),resy)
        print(mx,Mx,my,My,s_sel)
        img_L = cv2.imread(fname)[::ech,::ech,::]
        img_C = img_L[mx:Mx,my:My,::] #on doit avoir : 700 - 1200 / 0 -400
       # img_C = img_L[::2,::2,::]
    else : 
        img_C  = cv2.imread(fname)[::ech,::ech,::]     # Lecture image en couleurs BGR
    t0 = time.time()
    print(img_C.shape)
    #Etape 1 : égalisation  HSL
    # inutile pour le moment

    imgHSL= Egalisation_HSL_gold(img_C)
    
    t1 = time.time()
    print("Tps ega : ",t1 -t0 )
    #    cv2.namedWindow("Ega", cv2.WINDOW_NORMAL) 
#    cv2.imshow("Ega", img_egalisation)

    # Etape 2 : filtrage 
    # inutile pour le moment
 #   taille   = 7

  #  img_Gaus = img_egalisation.copy()
    
#    
#    cv2.namedWindow("Gaussian", cv2.WINDOW_NORMAL) 
#    cv2.imshow("Gaussian", img_Gaus)

#img_egalisation = img_Gaus
# Init des seuils 


    Hmin =0
    Hmax = 255
    Smin =0
    Smax = 38
    Lmin = 242
    Lmax = 255
    k1 =1
    kf = 2*k1 + 1 
    k2 =1
    ko = 2*k2 + 1 
 
    
    lower = np.array([Hmin,Lmin,Smin])
    upper = np.array([Hmax,Lmax,Smax])
    img_bin = cv2.inRange(imgHSL,lower,upper)
        
    #def hist_func(param, lower, upper):
    #    return cv2.inRange(param, lower, upper)
    #th1 = Threading.Thread(target=hist_func, args=param, lower, upper)
    #th1.start()
    #th1.join()
    #img_calc = cv2.bitwise_and(imgHSL,imgHSL,mask = img_bin)
        
    
    #img =  cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    #cv2.namedWindow('Masque',cv2.WINDOW_NORMAL)
    #cv2.imshow('Masque',img_bin)
    t2 = time.time()
    print("Tps filtrage : ", t2-t1)
    kernelf = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kf, kf))
    kernelo = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ko, ko))
#
#
#    
#    
    et1 = cv2.morphologyEx(img_bin, cv2.MORPH_CLOSE, kernelf)
   # img5 = cv2.bitwise_and(img_calc,img_calc,mask=et1)
    et2 = cv2.morphologyEx(et1, cv2.MORPH_OPEN, kernelo)
    #img3 = cv2.bitwise_and(img5,img5,mask=et2)


   # cv2.imshow('Ap opening',et2)
    t3 = time.time()
    print("Tps ouverture / fermeture : ", t3 -t2)
    imgfinal = img_C.copy()

    contours, hierarchy = cv2.findContours(et2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #[1:]
    cv2.drawContours(imgfinal, contours, -1, (255,255,0), 1, cv2.LINE_8, hierarchy)
    cv2.imshow("image contours",imgfinal)
    cx,cy = 0,0
    T = 0
    v_seuil = 5000/(ech**2) #(4**ech)#50000/(ech*ydist)
    print(v_seuil)
    for i in range (len(contours)):
        cnt = contours[i]
        M = cv2.moments(cnt)
        if M['m00'] > v_seuil:
            cx = int(M['m10']/(M['m00']+1*10**-5))
            cy = int(M['m01']/(M['m00']+1*10**-5))
            print(M['m00'])
            cv2.circle(imgfinal,(cx,cy), 4, (0,0,255), -1) 
            #(x,y),(Ma,ma),angle =  cv2.fitEllipse(cnt)
            #angle : angle de rotation de l'ellipse.
          
            #area = cv2.contourArea(cnt)
            #x,y,w,h = cv2.boundingRect(cnt)
            #rect_area = w*h
            #extent = float(area)/rect_area
            T += 1
            break
                
        
#    if T == 0 : 
#        print("Circle meth")
#        circles = cv2.HoughCircles(et2, cv2.HOUGH_GRADIENT,2.3,minDist = 100)
#        if circles is not None:
#            circles = np.round(circles[0, :]).astype("int")
#            for (x, y, r) in circles:
#                cv2.circle(img_C, (x, y), r, (0, 255, 0), 4)
#                cv2.rectangle(img_C, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)


# matlab : regionprops : connaître aire, excentricité, ... 
# à partir moment, trouver excentricité ou trouver formule mathématiques pour connaître excentricité avec moments (uv 5.5)
# essayer fit ellipse pour trouver excentricité, 


##### FIN
    print("Tps pour détection cerlce : ", time.time() - t3)
    print("Tps exécution total: ", time.time() - t0)
#    print("Angle : ", angle)
#    print("Major axis : ", Ma)
#    print("Minor aixs : ",ma)
#    print(extent)
    # réfléchir à diminuer zone de détection ap 1e détection, afin d'aller + vite
  #  cx, cy = cy,cx
    test_im = img_C.copy()
    cv2.circle(test_im,(cx,cy), 4, (0,0,255), -1)
    print("center is ({},{})".format(cy, cx))
    cv2.imshow("image centroides",test_im)
    cv2.waitKey(0)                     
    cv2.destroyAllWindows()
    height,width = img_C.shape[0:2]
    pos_s_x = height/2
    pos_s_y = width/2
    print(height,width)
    return([cy,cx],[cy-pos_s_y,cx-pos_s_x],[height,width])


def detect_color(fname,ech,ydist,resx = 0,resy = 0,L = [],avan_y = 0): 
    if L != []:
        cx = L[0]
        cy = L[1]
        s_sel = min(resx,resy)/2
        mx = max(int(cx-s_sel),0)
        Mx = min(int(cx+s_sel),resx)
        my = max(int(cy-s_sel-avan_y),0)
        My = min(int(cy+s_sel-avan_y),resy)
        print(mx,Mx,my,My,s_sel)
        img_L = cv2.imread(fname)[::ech,::ech,::]
        img_C = img_L[mx:Mx,my:My,::] #on doit avoir : 700 - 1200 / 0 -400
       # img_C = img_L[::2,::2,::]
    else : 
        img_C  = cv2.imread(fname)[::ech,::ech,::]     # Lecture image en couleurs BGR
    t0 = time.time()
    print(img_C.shape)
    
    #Etape 1 : égalisation  HSL
    # inutile pour le moment

    #img_egalisation = Egalisation_HSL_col(img_C)
    #    cv2.namedWindow("Ega", cv2.WINDOW_NORMAL) 
#    cv2.imshow("Ega", img_egalisation)

    # Etape 2 : filtrage 
    # inutile pour le moment
 #   taille   = 7

  #  img_Gaus = img_egalisation.copy()
    
#    
#    cv2.namedWindow("Gaussian", cv2.WINDOW_NORMAL) 
#    cv2.imshow("Gaussian", img_Gaus)

#img_egalisation = img_Gaus
# Init des seuils 


    imgHSL = cv2.cvtColor(img_C,cv2.COLOR_BGR2HLS)

    if color == "G":
        Hmin = 30
        Hmax = 100
        Smin = 35
        Smax = 255
        Lmin = 33
        Lmax = 255
        k1 =1
        kf = 2*k1 + 1 
        k2 =1
        ko = 2*k2 + 1 
    
    elif color == "R":
        Hmin = 120
        Hmax = 255
        Smin = 54
        Smax = 255
        Lmin = 33
        Lmax = 255
        k1 =1
        kf = 2*k1 + 1 
        k2 =1
        ko = 2*k2 + 1 


    elif color == "B":
        Hmin = 50
        Hmax = 157
        Smin  = 53
        Smax = 255
        Lmin = 40
        Lmax = 255
        k1 =1
        kf = 2*k1 + 1 
        k2 =1
        ko = 2*k2 + 1 
    
    lower = np.array([Hmin,Lmin,Smin])
    upper = np.array([Hmax,Lmax,Smax])
        
    img_bin = cv2.inRange(imgHSL,lower,upper)
    #img_calc = cv2.bitwise_and(imgHSL,imgHSL,mask = img_bin)
        
    
    #img =  cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
   # cv2.namedWindow('Masque',cv2.WINDOW_NORMAL)
   # cv2.imshow('Masque',img_bin)
        
#    kernelf = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kf, kf))
#    kernelo = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ko, ko))
#
#
#    
#    
#    et1 = cv2.morphologyEx(img_bin, cv2.MORPH_CLOSE, kernelf)
#    img5 = cv2.bitwise_and(img_calc,img_calc,mask=et1)
#    et2 = cv2.morphologyEx(et1, cv2.MORPH_OPEN, kernelo)
#    img3 = cv2.bitwise_and(img5,img5,mask=et2)


   # cv2.imshow('Ap opening',et2)
 
    #imgfinal = img_C.copy()

    contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #[1:]
    #cv2.drawContours(imgfinal, contours, -1, (255,255,0), 1, cv2.LINE_8, hierarchy)
    #cv2.imshow("image contours",imgfinal)

    T = 0
    L = []
    for i in range (len(contours)):
        cnt = contours[i]
        M = cv2.moments(cnt)
        if M['m00'] > 300:
            cx = int(M['m10']/(M['m00']+1*10**-5))
            cy = int(M['m01']/(M['m00']+1*10**-5))
            L.append([cx,cy])
            #print(M['m00'])
            #cv2.circle(img_C,(cx,cy), 4, (0,0,255), -1) 
            #(x,y),(Ma,ma),angle =  cv2.fitEllipse(cnt)
            #angle : angle de rotation de l'ellipse.
          
            #area = cv2.contourArea(cnt)
            #x,y,w,h = cv2.boundingRect(cnt)
            #rect_area = w*h
            #extent = float(area)/rect_area
            T += 1
            if T > 1 :
                #print(T)
                break
                
        
#    if T == 0 : 
#        print("Circle meth")
#        circles = cv2.HoughCircles(et2, cv2.HOUGH_GRADIENT,2.3,minDist = 100)
#        if circles is not None:
#            circles = np.round(circles[0, :]).astype("int")
#            for (x, y, r) in circles:
#                cv2.circle(imgfinal, (x, y), r, (0, 255, 0), 4)
#                cv2.rectangle(img_C, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
#    
    

# matlab : regionprops : connaître aire, excentricité, ... 
# à partir moment, trouver excentricité ou trouver formule mathématiques pour connaître excentricité avec moments (uv 5.5)
# essayer fit ellipse pour trouver excentricité, 


##### FIN
    print("Tps exécution : ", time.time() - t0)
    #cv2.imwrite("Img_detec.jpg", img_C)    
    
#    print("Angle : ", angle)
#    print("Major axis : ", Ma)
#    print("Minor aixs : ",ma)
#    print(extent)
    

    height,width = img_C.shape[0:2]
    pos_s_x = height/2
    pos_s_y = width/2
    mx,my = 100000,100000
    print(len(L))
    for k in range(len(L)):
        cv2.circle(img_C,(L[k][0],L[k][1]), 4, (0,0,255), -1) 
        if abs(L[k][0] -pos_s_x) < mx and abs(L[k][1] - pos_s_y) < my:
            mx = L[k][0]-pos_s_x
            my  = L[k][1] - pos_s_y
            cx = L[k][0]
            cy = L[k][1]
    cv2.imshow("image centroides",img_C)
    cv2.waitKey(0)                     
    cv2.destroyAllWindows()
    return([cy,cx],[my,mx],[height,width])

if __name__ == "__main__":
    #detect_color("col_29_04_0.jpg","B")
    L,Lv, L_s= detect_gold("gold_29_04_1.jpg",8,250)
    print(L,L_s)
    detect_gold("gold_29_04_1.jpg",8,250,L_s[0],L_s[1],L,0)