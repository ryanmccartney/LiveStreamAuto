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


while 1:   
    text = "Now viewing "

    selectedScene = liveStream.selectRandomScene()

    liveStream.changeScene(selectedScene)

    text = text + liveStream.currentView

    liveStream.banner_text = text

    delay = liveStream.selectRandomLength()
    time.sleep(delay)