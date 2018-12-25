#NAME:  stream.py
#DATE:  25/12/2018
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python class for aquiring and analysising image data from network streams
#COPY:  Copyright 2018, All Rights Reserved, Ryan McCartney

import threading
import numpy as np
import cv2 as cv
import time
import imutils
import json
import random
import datetime
import requests

#define threading wrapper
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class stream:

    banner_text = "Starting Text"
    currentView = "None"
    nightLength = ""
    sunset = ""
    sunrise = ""
    sunsetText = ""
    sunriseText = ""
    objects = 0

    def __init__(self, settings_location, minShotLength, maxShotLength):

        #Load user adjustable variables from json file
        settingsFile = open(settings_location).read()
        
        self.settings = json.loads(settingsFile)
        self.NumberOfStreams = len(self.settings["shots"])
        self.NumberOfStreams = self.NumberOfStreams -1

        self.minShotLength = minShotLength
        self.maxShotLength = maxShotLength

        self.startScene = self.settings["title"][0]["scene"]
        self.currentScene = self.startScene

    def getSeconds(self,time_str):
        h, m, s = time_str.split(':')

        return int(h) * 3600 + int(m) * 60 + int(s)

    @threaded
    def getTime(self):
    
        while 1:
            #Get time stamp
            ts = time.gmtime()
            print(time.strftime("TIME: %H:%M:%S", ts))
    
            #Write to file
            file = open(self.settings["fileStore"][0]["clockFileLocation"],'w') 
            file.write(time.strftime("%H:%M:%S", ts)) 
            file.close()
            time.sleep(0.5) 

    @threaded
    def textRender(self):
        
        current_text = ""

        while 1:

            if self.banner_text != current_text:

                #Write Banner Text to file
                file = open(self.settings["fileStore"][0]["bannerTextFileLocation"],'w') 
                file.write(self.banner_text) 
                file.close()

                print("TEXT: Text written to stream banner '",self.banner_text,"'")
                current_text= self.banner_text 
           
    @threaded
    def streamProgram (self):
        
        stream_url = ""

        while 1:
            
            programScene = self.currentScene
            shots = len(self.settings['shots'])

            #Search for the URL of that stream
            for i in range(shots):

                if self.settings['shots'][i]['scene'] == programScene:
                    stream_url = self.settings['shots'][i]['url']
                    print("STREAM: The program scene is ",programScene," and the URL is ",stream_url)
                    break
                else:
                    stream_url = ""
                    
            if stream_url != "":
                
                stream = cv.VideoCapture(stream_url)
             
                # initialize the first frame in the video stream
                firstFrame = None

                while self.currentScene == programScene:

                    ret, frame = stream.read()
                    self.objects = 0
                    minArea = 2

                    if frame is not None:
                        # resize the frame, convert it to grayscale, and blur it
                        frame = imutils.resize(frame, width=500)
                        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                        gray = cv.GaussianBlur(gray, (21, 21), 0)

	                    # if the first frame is None, initialize it
                        if firstFrame is None:
                            firstFrame = gray
                            continue
                    
                        # compute the absolute difference between the current frame and first frame
                        frameDelta = cv.absdiff(firstFrame, gray)
                        thresh = cv.threshold(frameDelta, 25, 255, cv.THRESH_BINARY)[1]
 
	                    # dilate the thresholded image to fill in holes, then find contours on thresholded image
                        thresh = cv.dilate(thresh, None, iterations=2)
                        cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
                        cnts = imutils.grab_contours(cnts)
 
	                    # loop over the contours
                        for c in cnts:
		                    # if the contour is too small, ignore it
                            if cv.contourArea(c) < minArea:
                                continue
 
		                    # compute the bounding box for the contour, draw it on the frame,
		                    # and update the qtext
                            (x, y, w, h) = cv.boundingRect(c)
                            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            self.objects = self.objects + 1

                        cv.imshow('Program Output',frame)
                        key = cv.waitKey(1) & 0xFF

                        if key == ord("q"):
                            break
 
                #cleanup the camera and close any open windows
                stream.release()
                cv.destroyAllWindows()
  
    def selectRandomScene (self):
               
        sceneNumberSelected = random.randint(0,self.NumberOfStreams)
        self.currentScene = self.settings["shots"][sceneNumberSelected]["scene"]
        self.currentView = self.settings["shots"][sceneNumberSelected]["view"]

        return self.currentScene

    def selectRandomLength (self):

        shotLength = random.randint(self.minShotLength,self.maxShotLength)

        return shotLength

    def changeScene (self, scene):

        #Write Selected Scene to .txt file
        file = open(self.settings["fileStore"][0]["currentScene"],'w') 
        file.write(scene) 
        file.close()

        self.currentScene = scene        
        print("SCENE: The Program scene has been changed to '",scene,"'")

    def getSunsetSunrise (self):

        #Build URL with info from the settings file
        url = self.settings["sunsetsunrise"][0]["url"] 
        long = self.settings["sunsetsunrise"][0]["longitude"] 
        lat = self.settings["sunsetsunrise"][0]["latitude"] 

        date = datetime.date.today().strftime("%Y-%m-%d")
        
        url = url + "json?lat=" + lat  + "&lng=" + long + "&date=" + date

        response = requests.get(url)
        data = response.json()

        #Display Response Sunrise and Sunset Time
        print("INFO: The Sunrise is at",data["results"]["sunrise"],"and the Sunset is at",data["results"]["sunset"])

        #Write Selected Scene to .json file
        file = open(self.settings["fileStore"][0]["sunsetsunrise"],'w') 
        file.write(response.content.decode("utf-8")) 
        file.close()

        self.sunset = date + " " + data["results"]["sunset"] 
        self.sunrise = date + " " + data["results"]["sunrise"]
        self.nightLength = data["results"]["day_length"]

        self.sunsetText = data["results"]["sunset"] 
        self.sunriseText = data["results"]["sunrise"]

        format = ("%Y-%m-%d %I:%M:%S %p")
        self.sunset = int(time.mktime(time.strptime(self.sunset, format)))
        self.sunrise = int(time.mktime(time.strptime(self.sunrise, format)))

        self.nightLength = self.getSeconds(self.nightLength)
        self.nightLength = self.getSeconds("24:00:00") - self.nightLength 