from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import datetime
import json
import imutils
import cv2 as cv


def dataLoad():
    with open('scripts/scenes.json') as f:
        fileContents = json.load(f)
    return fileContents

while(1):


    data = dataLoad()
              
    streamNumber = len(data["shots"])

    for i in range(0,streamNumber):

        #Initialize the first frame in the video stream
        firstFrame = None

        image = cv.VideoCapture(data["shots"][i]["url"])

        ret, frame = image.read()
        #frame = imutils.resize(frame, width=min(500, frame.shape[1]))
    
        text = "No Movement Detected"
  
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (21, 21), 0)
 
        # if the first frame is None, initialize it
        if firstFrame is None:
	        firstFrame = gray
	        continue

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv.absdiff(firstFrame, gray)
        thresh = cv.threshold(frameDelta, 25, 255, cv.THRESH_BINARY)[1]
 
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv.dilate(thresh, None, iterations=2)
        cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL,
	        cv.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
 
        # loop over the contours
        for c in cnts:
	        # if the contour is too small, ignore it
	        if cv.contourArea(c) < 10:
		        continue
 
	        # compute the bounding box for the contour, draw it on the frame,
	        # and update the text
	        (x, y, w, h) = cv.boundingRect(c)
	        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	        text = "Movement Detected"

        # draw the text and timestamp on the frame
        cv.putText(frame, "Status: {}".format(text), (10, 20),
	        cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
	        (10, frame.shape[0] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
 
        # show the frame and record if the user presses a key
        cv.imshow("Bird Camera Stream", frame)
    
        #Uncomment Below lines to see threshold image
        cv.imshow("Thresh", thresh)
        cv.imshow("Frame Delta", frameDelta)
    
        key = cv.waitKey(1) & 0xFF    
    
        #Close on ESC
        k = cv.waitKey(5) & 0xFF
        if k == 27:
            break
            
cv.destroyAllWindows()