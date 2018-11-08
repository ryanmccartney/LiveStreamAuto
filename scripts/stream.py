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
    currentScene = "Start Title"

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

                print("TEXT: Text written to stream banner '",self.banner_text,"'")
                current_text= self.banner_text 
           
    @threaded
    def streamProgram (self):
        
        stream_url = ""

        while 1:
            
            #Search for the URL of that stream
            for i in self.settings['shots']:
                if i['scene'] == self.currentScene:
                    stream_url = i['url']

            print("STREAM: The program scene is ",self.currentScene," and the URL is ",stream_url)

            stream = cv.VideoCapture(stream_url)

            programScene = self.currentScene

            while self.currentScene == programScene:

                ret, frame = stream.read()
                cv.imshow('Program Output',frame)

                k = cv.waitKey(5) & 0xFF

                if k == 27:
                    break
        
            stream.release()

    def selectRandomScene (self):
               
        sceneNumberSelected = random.randint(0,self.NumberOfStreams)
        self.currentScene = self.settings["shots"][sceneNumberSelected]["scene"]

        return self.currentScene

    def selectRandomLength (self):

        shotLength = random.randint(self.minShotLength,self.maxShotLength)

        return shotLength

    def changeScene (self, scene):

        #Write Selected Scene to .txt file
        file = open(self.settings["fileStore"][0]["currentScene"],'w') 
        file.write(scene) 
        file.close()

        print("SCENE: The Program scene has been changed to '",scene,"'")