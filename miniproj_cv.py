#***********************************************************
# Name: Kristen Ung
# Date: Sept , 2021
# Title: EENG350_Assignment2.py
#
#***********************************************************
#
# Assignment 2 : Using OpenCV
#
# The purpose of this assignment is to gain experience with
# OpenCV and image processing. The assignment is split into
# 6 functions, each with a different purpose. The program
# prompts the user with which program they would like to
# execute.
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
    
    for i in range(10):
    #camera.capture('img' + str(i)+'.png')
        gains.append(camera.awb_gains)
#    print("img " + str(i))
#    print(gains)
    
    g0 = np.mean(gains[0])
    g1 = np.mean(gains[1])
    print(str(g0) + ", " + str(g1))


    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    camera.awb_mode = 'off'
    camera.awb_gains = [g0, g1]
    
    return camera
    

def capture_angle(camera):
    
    rawCapture = PiRGBArray(camera)
    
    try:
        camera.capture(rawCapture, format="rgb")
        image = rawCapture.array
        image = image[:,:,::-1]
    except:
        print("Failed to capture")

    try:
        cv.imwrite('colorDetect.jpg', image)
    except:
        print('Save Failed')
        pass
    
    
    img = cv.imread('colorDetect.jpg',1)
    img = cv.resize(img, None, fx=0.5, fy=0.5, interpolation = cv.INTER_CUBIC)

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    
    lower = np.array([70, 100, 100], dtype = "uint8")
    upper = np.array([230, 230, 200], dtype = "uint8")

    mask = cv.inRange(hsv, lower, upper)

    res = cv.bitwise_and(img, img, mask = mask)
    
    
    kernel = np.ones((5,5),np.uint8)
    erosion = cv.erode(res,kernel,iterations = 1)
    
    dilation = cv.dilate(erosion,kernel,iterations=1)
    
    grayscale = cv.cvtColor(dilation, cv.COLOR_BGR2GRAY)
    
    ret,thresh = cv.threshold(grayscale,50,255,cv.THRESH_BINARY)
    
    arr = np.array(thresh)
    arr = np.nonzero(arr)
    locateX = np.mean(arr[1])
    locateY = np.mean(arr[0])
    
    angle = 27*(locateX - 480)/480
    
    rawCapture.truncate()
    rawCapture.seek(0)
    
    return angle
  