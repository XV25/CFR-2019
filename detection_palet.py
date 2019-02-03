from __future__ import division
import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
	# frame = cv2.imread('image_test2.jpg')

    frameBGR = cv2.GaussianBlur(frame,(5, 5),0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    v = cv2.extractChannel(hsv, 0)
    											# on choisi la couleur du palet a detecter
    mask = cv2.inRange(v,170,179) # red 
    # mask = cv2.inRange(v,55,70) # green
    # mask = cv2.inRange(v,90,100) # blue
    

    kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))

    mask_m = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open, iterations = 3)
    mask_m = cv2.morphologyEx(mask_m, cv2.MORPH_CLOSE, kernel_close, iterations = 3)

    cv2.imshow('mask_m', mask_m)

    ref,contours,hierachy=cv2.findContours(mask_m,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    galet_position = [0., 0.]
    galet_found = False

    list_center=[]
    for c in contours:
		# calculate moments for each contour
        M = cv2.moments(c)
		 
		# calculate x,y coordinate of center
        if(M["m00"] != 0 and  M["m00"] != 0):
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            list_center.append([cY, cX])
            cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, "("+str(cY)+","+str(cX)+")", (cX, cY+5), font, 1, (255, 255, 0), 2, cv2.LINE_AA)

    if len(list_center) > 0:
        galet_found = True
        list_center_np = np.array(list_center)

        index_max = np.argmax(list_center_np, axis=0)
        position_max = list_center_np[index_max[0]]

        center_image_X = mask_m.shape[1]/2
        galet_error_X = position_max[1] - center_image_X

        print(list_center_np, index_max, position_max, galet_error_X)		# galet_error_X contient la distance du galet le plus proche au centre de l'image

        # cv2.line(frame, (position_max[0], 0), (position_max[0], mask_m.shape[1]), (255, 0, 0), 5)
    
    #print(galet_procheX,galet_procheY)
    
    # if dist_Galet != 120000:
    #     print("la distance est de ")
    #     print(dist_Galet)


     cv2.imshow('frame', frame)
     cv2.imshow('mask', mask)
    # cv2.imshow('v', v)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #time.sleep(0.2)
cap.release()
cv2.destroyAllWindows()
