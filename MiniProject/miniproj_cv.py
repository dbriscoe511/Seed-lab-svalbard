#***********************************************************
# Name: Kristen Ung & Xander Bahr
# Date: Sept , 2021
# Title: miniproj_cv.py
#
#***********************************************************
#
# The purpose of this assignment is to develop a computer
# vision algorithm that is able to notify main as to the 
# angle of rotation needed to face a specific marker
#
#************************************************************

from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import cv2 as cv
import numpy as np
import math


def setup_camera():
    #sleep(1)
    camera = PiCamera()
    sleep(1)
    
    
    return camera

def calibrate(camera):
    gains = []
    for i in range(10):
        gains.append(camera.awb_gains) #Takes 10 "pictures" and gets the auto white balance gains of each
    
    g0 = np.mean(gains[0]) #Average the gains captured
    g1 = np.mean(gains[1])
    print(str(g0) + ", " + str(g1))


    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    camera.awb_mode = 'off'
    camera.awb_gains = [g0, g1] #Sets the awb gains to be the captured values
    
    return camera
    

def capture_angle(camera):
    
    rawCapture = PiRGBArray(camera)    # Initializes rawCapture
    
    try:
        camera.capture(rawCapture, format="rgb")    # Takes image
        image = rawCapture.array                    # Stores image in array
        image = image[:,:,::-1]                     # Manually flips bits (Broken Camera)
    except:
        print("Failed to capture")

    try:
        cv.imwrite('colorDetect.jpg', image)        # Saves image for reference
    except:
        print('Save Failed')
        pass
    
    
    img = cv.imread('colorDetect.jpg',1)    # Reads image
    img = cv.resize(img, None, fx=0.5, fy=0.5, interpolation = cv.INTER_CUBIC)    # Resizes the image to be smaller than screen

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)      # Converts image to HSV
    
    lower = np.array([70, 100, 100], dtype = "uint8")     # lower mask limit for isolating blue
    upper = np.array([230, 230, 200], dtype = "uint8")    # higher mask limit for isolating blue

    mask = cv.inRange(hsv, lower, upper)   # generates mask

    res = cv.bitwise_and(img, img, mask = mask)    # Masks the image using bitwise and
    
    
    kernel = np.ones((5,5),np.uint8)           # Sets kernel size
    
    # Image processing for filling image
    
    erosion = cv.erode(res,kernel,iterations = 1)
    
    dilation = cv.dilate(erosion,kernel,iterations=1)
    
    grayscale = cv.cvtColor(dilation, cv.COLOR_BGR2GRAY)     # Converts to grayscale
    
    ret,thresh = cv.threshold(grayscale,50,255,cv.THRESH_BINARY)   # Performs thresholding
    
    arr = np.array(thresh)       # Converts threshold to numPy
    arr = np.nonzero(arr)        # Nonzeros the numPy array
    locateX = np.mean(arr[1])    # Finds center of marker
    locateY = np.mean(arr[0])
    
    angle = 27*(locateX - 480)/480    # Finds angle needed to turn
    
    rawCapture.truncate()    # Clears raw capture
    rawCapture.seek(0)
    
    return angle       # Returns angle to main
  