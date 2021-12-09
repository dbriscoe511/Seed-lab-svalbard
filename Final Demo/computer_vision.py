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
    
    #Constants for changing brightness and contrast
    alpha = 1 #Contrast Value
    beta = 40    #Brightness Value
    

    #set camera with calibrated gains
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 60
    #camera.iso = 800
    
    g0 = np.mean(gains[0])
    g1 = np.mean(gains[1])
    camera.awb_mode = 'off'
    #camera.awb_gains = [g0, g1]
    camera.awb_gains = [g0, g1]
    
    stream = PiRGBArray(camera)
    sleep(0.1)
    #take video and modify each frame
    for foo in camera.capture_continuous(stream, format='bgr', use_video_port=True):
        stream.truncate()
        stream.seek(0)
        frame = stream.array
        frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
        #isolate blue
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower = np.array([110, 85, 60])
        upper = np.array([140, 255, 255])
        
        mask = cv2.inRange(hsv, lower, upper)
        results = cv2.bitwise_and(frame, frame, mask=mask)
        
        kernel = np.ones((20,20),np.uint8)
        closed = cv2.morphologyEx(results, cv2.MORPH_CLOSE, kernel)
        smoothed = cv2.medianBlur(closed,5)
        smoothed = smoothed[240:400, 0:640]
        
        grayscale = cv2.cvtColor(smoothed, cv2.COLOR_BGR2GRAY)     # Converts to grayscale
        
        ret,thresh = cv2.threshold(grayscale,10,255,cv2.THRESH_BINARY)   # Performs thresholding
        
        
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
            bottommost = tuple(contours[contours[:,:,1].argmax()][0])
            rightmost = tuple(contours[contours[:, :, 0].argmax()][0])
            leftmost = tuple(contours[contours[:, :, 0].argmin()][0])
            # Finds various extreme points of the tape
            M = cv2.moments(contours)
            bX = bottommost[0]
            rX = rightmost[0]
            lX = leftmost[0]
            rY = rightmost[1]
            lY = leftmost[1]
            tX = topmost[0]
            tY = topmost[1] 
            
            cX = tX
            cY = tY
            if M['m00'] != 0:
                cX = int(M['m10']/M['m00'])
                if cX < 320:
                    cX = cX + 20
                
                #cY = int(M['m01']/M['m00'])
            
            cX2 = int((rX - lX) / 2 + lX)
            
    
                
            cv2.circle(smoothed, (cX, cY), 7, (0, 0, 255))
            cv2.circle(smoothed, (rX, rY), 7, (0, 0, 255))
            cv2.circle(smoothed, (lX, lY), 7, (0, 0, 255))
                
        if cX != None:
            angle = 27*(cX - 320)/320    # Finds angle needed to turn
            #if float(angle) > 15:
            #    angle = '15'
            #if float(angle) < -15:
            #    angle = '-15'
        else:
            angle = 'No line detected'
        
        
        if cY != None:
            #Detects end of the tape if it sees a plus.
            if (abs(rX - lX) >= 180) and (rY >= 55 and lY >= 55) and (rY >= 110 or lY >= 110) and (rX > 550 or lX < 90) and (min(abs(rY - tY), abs(lY - tY)) >= 50) and (abs(lY - rY) <= 120) and (tY <= 60) and (max(abs(rY - tY), abs(lY - tY)) >= 110):
                sys.stdout.write('stop\n')
            else:
                sys.stdout.write(str(angle) + '\n')
            
        else:
            sys.stdout.write(str(angle) + '\n')
        sys.stdout.flush()
        cv2.imshow('frame', smoothed)
        #cv2.imshow('img', frame)
         #cv2.imshow('thresh', thresh)
                                  
        if cv2.waitKey(1) == ord('q'):
            break
        
    cv2.destroyAllWindows()
