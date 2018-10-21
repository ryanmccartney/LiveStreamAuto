from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import datetime
import imutils
import cv2

image = cv2.VideoCapture("rtsp://192.168.1.114:554/11")

# initialize the first frame in the video stream
firstFrame = None

while(1):

    ret, frame = image.read()
    frame = imutils.resize(frame, width=min(500, frame.shape[1]))
    
    text = "No Movement Detected"
  
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
 
    # if the first frame is None, initialize it
    if firstFrame is None:
	    firstFrame = gray
	    continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	    cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
 
    # loop over the contours
    for c in cnts:
	    # if the contour is too small, ignore it
	    if cv2.contourArea(c) < 10:
		    continue
 
	    # compute the bounding box for the contour, draw it on the frame,
	    # and update the text
	    (x, y, w, h) = cv2.boundingRect(c)
	    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	    text = "Movement Detected"

    # draw the text and timestamp on the frame
    cv2.putText(frame, "Status: {}".format(text), (10, 20),
	    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
	    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
 
    # show the frame and record if the user presses a key
    cv2.imshow("Bird Camera Stream", frame)
    
    #Uncomment Below lines to see threshold image
    #cv2.imshow("Thresh", thresh)
    #cv2.imshow("Frame Delta", frameDelta)
    
    key = cv2.waitKey(1) & 0xFF    
    
    #Close on ESC
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
            
cv2.destroyAllWindows()