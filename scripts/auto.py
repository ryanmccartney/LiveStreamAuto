
import time
import datetime
import json
import random
from pprint import pprint
import threading

#Limits for the length of a shot
minShotLength = 3
maxShotLength = 15
currentScene = ""
ts = 0
data = ""

def time():
    
    while 1:
        #Get time stamp
        ts = time.gmtime()
        print(time.strftime("TIME: %H:%M:%S", ts))
    
        #Write to file
        file = open('time.txt','w') 
        file.write(time.strftime("%H:%M:%S", ts)) 
        file.close()

#Load data from scenes.json
def dataLoad():
    with open('scenes.json') as f:
        data = json.load(f)

while 1:
    
    dataLoad()
    shotLength = random.randint(minShotLength,maxShotLength)


    angles = len(data['shots'])
    angles = angles - 1
    sceneNumberSelected = random.randint(0,angles)
    currentScene = data["shots"][sceneNumberSelected]["scene"]

    #Write Selected Scene to .txt file
    file = open('scene.txt','w') 
    file.write(currentScene) 
    file.close()

    #Write Banner Text to file
    file = open('bannerText.txt','w') 
    file.write(time.strftime("The current time is %H:%M:%S.", ts)) 
    file.close()

    #Some infor before sleeping for a while
    print("INFO: The length of the scene ",currentScene," will be ",shotLength," seconds.")

    #Wait for half a second before checking the time again
    time.sleep(shotLength) 



   