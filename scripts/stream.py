#NAME:  stream.py
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

#define threading wrapper
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class stream:

    banner_text = "Starting Text"

    def __init__(self, settings_location, minShotLength, maxShotLength):

        #Load user adjustable variables from json file
        settingsFile = open(settings_location).read()
        
        self.settings = json.loads(settingsFile)
        self.NumberOfStreams = len(self.settings["shots"])
        self.NumberOfStreams = self.NumberOfStreams -1

        self.minShotLength = minShotLength
        self.maxShotLength = maxShotLength

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

                current_text= self.banner_text 

    def selectRandomScene (self):
               
        sceneNumberSelected = random.randint(0,self.NumberOfStreams)
        currentScene = self.settings["shots"][sceneNumberSelected]["scene"]
    
        return currentScene

    def selectRandomLength (self):

        shotLength = random.randint(self.minShotLength,self.maxShotLength)

        return shotLength