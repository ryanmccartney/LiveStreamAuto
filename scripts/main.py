#NAME:  main.py
#AUTH:  Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC:  A python class for aquiring image data from network streams
#COPY:  Copyright 2018, All Rights Reserved, Ryan McCartney

from stream import stream
from threading import Thread
from queue import Queue
import cv2 as cv
import json
import time
import random

settings_location = "scripts/settings.json"
minShotLength = 3
maxShotLength = 15

# Class instances for various streams
liveStream = stream(settings_location,minShotLength,maxShotLength)

#Start Clock
liveStream.getTime()

#Start Text Render
liveStream.textRender()

#Start programStream
#liveStream.streamProgram()

setScene = False
setBanner = False
delay = 10
text = ["Changing angle in X seconds","Now view A SHOT DESCRIPTION","The Stream ends today at XX:XX:XX PM","The Stream starts at XX:XX:XX PM","Nature Stream of Garden Birds Feeding","It's nightime, we'll be back in the morning"]
textItems = len(text)

while 1:   

    #Get Sunrise and Sunset Times
    liveStream.getSunsetSunrise()
    text[2] = "The Stream ends today at " + liveStream.sunsetText
    text[3] = "Stream returns at " + liveStream.sunriseText

    #Set openning text
    textSelected = 4
    liveStream.banner_text = text[textSelected]
    time.sleep(0.5)

    #Stream starts on the title
    selectedScene = liveStream.startScene
    liveStream.changeScene(selectedScene)
    time.sleep(delay)

    #If it's daytime
    while (time.time() > liveStream.sunrise) and (time.time() < liveStream.sunset):
        
        if setScene == False:
            setScene = True
            sceneStart = time.time()
            selectedScene = liveStream.selectRandomScene()
            delay = liveStream.selectRandomLength()
            liveStream.changeScene(selectedScene)

            text[1] = "Now viewing " + liveStream.currentView
            #Set Possible Text

        if time.time() > (sceneStart+delay):
            setScene = False

        if setBanner == False:
            setBanner = True
            textStart = time.time()
            textSelected = random.randint(0,(textItems-2))
            
        if time.time() > (textStart+3):
            setBanner = False
        
        #If Text has changed rerender
        if text[textSelected] != liveStream.banner_text:
            liveStream.banner_text = text[textSelected]
        
        text[0] = "Changing scene in " + str(int(delay-(time.time()-sceneStart))) + " seconds"

    sunset = liveStream.sunset

    #If it's nighttime
    while (time.time() > sunset) and (time.time() < liveStream.sunrise) :

        selectedScene = liveStream.startScene

        if liveStream.currentScene != selectedScene:
            liveStream.changeScene(selectedScene)

        if setBanner == False:
            setBanner = True
            textStart = time.time()
            textSelected = random.randint(3,(textItems-1))
            
        if time.time() > (textStart+5):
            setBanner = False
        
        #If Text has changed rerender
        if text[textSelected] != liveStream.banner_text:
            liveStream.banner_text = text[textSelected]
        