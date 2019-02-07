from __future__ import division
import cv2
import numpy as np
import time
cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    
    frameBGR = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(frameBGR, cv2.COLOR_BGR2HSV)
    v = cv2.extractChannel(hsv, 0)
    #mask = cv2.inRange(v,170,179) # red 
    #mask = cv2.inRange(v,55,70) # green
    mask = cv2.inRange(v,90,100) # blue
    

    kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))

    mask_m = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open, iterations = 3)
    mask_m = cv2.morphologyEx(mask_m, cv2.MORPH_CLOSE, kernel_close, iterations = 3)

    contours,hierachy=cv2.findContours(mask_m,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    list=[]
    dist_Galet= 120000
    for c in contours:
		# calculate moments for each contour
        M = cv2.moments(c)
		 
		# calculate x,y coordinate of center
        if(M["m00"] != 0 and  M["m00"] != 0):
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            list.append([cX, cY])
            if len(list) == 1:
                galet_procheY=cY
                galet_procheX=cX
                
            if cY > galet_procheY:
                galet_procheY=cY
                galet_procheX=cX
                
    dist_Galet = galet_procheX - mask_m.shape[1]/2

cap.release()
