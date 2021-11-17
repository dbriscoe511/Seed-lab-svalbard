from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep
import numpy as np
import cv2
import io
import sys
'''
This script takes a video and isolates blue tape. It then calculates the angle the robot needs to turn to be inline with the tape
'''

# Calibrate the awb of the camera
def camera_setup():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 60
    #camera.iso = 800
    gains = []
    sleep(0.1)
    for i in range(0, 10):
        gains.append(camera.awb_gains)

    

    camera.close()
    return gains
def cv_main(gains):
    #set camera with calibrated gains
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 60
    #camera.iso = 800
    
    g0 = np.mean(gains[0])
    g1 = np.mean(gains[1])
    camera.awb_mode = 'off'
    camera.awb_gains = [g0, g1]
    
    stream = PiRGBArray(camera)
    sleep(0.1)
    #take video and modify each frame
    for foo in camera.capture_continuous(stream, format='bgr', use_video_port=True):
        stream.truncate()
        stream.seek(0)
        frame = stream.array
        #isolate blue
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower = np.array([110, 85, 60])
        upper = np.array([140, 255, 255])
        
        mask = cv2.inRange(hsv, lower, upper)
        results = cv2.bitwise_and(frame, frame, mask=mask)
        
        kernel = np.ones((20,20),np.uint8)
        closed = cv2.morphologyEx(results, cv2.MORPH_CLOSE, kernel)
        smoothed = cv2.medianBlur(closed,5)
        smoothed = smoothed[100:480, 100:640]
        
        grayscale = cv2.cvtColor(smoothed, cv2.COLOR_BGR2GRAY)     # Converts to grayscale
        
        ret,thresh = cv2.threshold(grayscale,20,255,cv2.THRESH_BINARY)   # Performs thresholding
        
        
        #create contours
        cont_img, contours, hierarchies, = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        
        cX = None
        cY = None
        
        
        #only uise the largest contour and ignore ones too small
        if len(contours) != 0:
            contours = max(contours, key = cv2.contourArea)
            if cv2.contourArea(contours) < 30:
                contours = []
        
        if len(contours) != 0:
            cv2.drawContours(smoothed, contours, -1, (0, 255, 0), 2)
            #Isolate the topmost point of the line and offset by 30 pixels
            topmost = tuple(contours[contours[:,:,1].argmin()][0])
            cX = topmost[0]
            cY = topmost[1] - 30 #plus for max, - for min
            
            cv2.circle(smoothed, (cX, cY), 7, (0, 0, 255))
                
        if cX != None:
            angle = 27*(cX - 270)/270    # Finds angle needed to turn
        else:
            angle = 'No line detected'
        
        if cY != None:
            if cY > 580:
                sys.stdout.write('stop\n')
            else:
                sys.stdout.write(str(angle) + '\n')
            
        else:
            sys.stdout.write(str(angle) + '\n')
        sys.stdout.flush()
        cv2.imshow('frame', smoothed)
        cv2.imshow('img', frame)
        #cv2.imshow('thresh', thresh)
                                  
        if cv2.waitKey(1) == ord('q'):
            break
        
    cv2.destroyAllWindows()
