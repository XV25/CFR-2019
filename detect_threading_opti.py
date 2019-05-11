# -*- coding: utf-8 -*-
"""
Created on Sat May 11 10:58:57 2019

@author: ehnla
"""

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
from detect_auto_global_opti_max import * #nom du fichier dans lequel se trouvent les fonctions pour opencv
import cv2

class PiVideoStream:
    def __init__(self, resolution=(320, 240), framerate=32):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,format="bgr", use_video_port=True)
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

# import the necessary packages
#from __future__ import print_function

#from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS

import imutils
import time
import cv2
 
# construct the argument parse and parse the arguments

#ap.add_argument("-n", "--num-frames", type=int, default=100,
#	help="# of frames to loop over for FPS test")
display = 1
num_frames = 100
#ap.add_argument("-d", "--display", type=int, default=-1,
#	help="Whether or not frames should be displayed")
 
# initialize the camera and stream

# created a *threaded *video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from `picamera` module...")
vs = PiVideoStream().start()
time.sleep(2.0)
fps = FPS().start()
 
# loop over some frames...this time using the threaded stream
while fps._numFrames < num_frames:
	# grab the frame ffrom the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	#L,Lv,L_s = detect_gold_vid(frame,1,250)
	L,Lv,L_s = detect_color_vid(frame,"B",1,250)
	cv2.circle(frame,(L[1],L[0]), 4, (0,0,255), -1)
	# check to see if the frame should be displayed to our screen
	if display > 0:
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
 
	# update the FPS counter
	fps.update()
 
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
