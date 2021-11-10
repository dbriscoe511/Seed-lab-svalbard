from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep
import numpy as np
import cv2
import io
import sys

def camera_setup():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 15

    gains = []
    camera.start_preview()
    sleep(3)
    camera.stop_preview()
    for i in range(0, 10):
        gains.append(camera.awb_gains)

    

    camera.close()
    return gains
def cv_main(gains):
    
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 50
    g0 = np.mean(gains[0])
    g1 = np.mean(gains[1])
    camera.awb_mode = 'off'
    camera.awb_gains = [g0, g1]
    
    stream = PiRGBArray(camera)
    sleep(0.1)
    
    for foo in camera.capture_continuous(stream, format='bgr', use_video_port=True):
        stream.truncate()
        stream.seek(0)
        frame = stream.array
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower = np.array([50, 50, 50])
        upper = np.array([130, 255, 255])
        
        mask = cv2.inRange(hsv, lower, upper)
        results = cv2.bitwise_and(frame, frame, mask=mask)
        
        kernel = np.ones((5,5),np.uint8)
        closed = cv2.morphologyEx(results, cv2.MORPH_CLOSE, kernel)
        smoothed = cv2.medianBlur(closed,5)
        #smoothed = cv2.dilate(smoothed, kernel, iterations=3)
        smoothed = smoothed[300:480, 0:640]
        
        grayscale = cv2.cvtColor(smoothed, cv2.COLOR_BGR2GRAY)     # Converts to grayscale
        
        ret,thresh = cv2.threshold(grayscale,0,255,cv2.THRESH_BINARY)   # Performs thresholding
        
        
        
        cont_img, contours, hierarchies, = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        cX = None
        cY = None
        
        if len(contours) != 0:
            contours = max(contours, key = cv2.contourArea)
        
        if len(contours) != 0:
            cv2.drawContours(smoothed, contours, -1, (0, 255, 0), 2)
            #for c in contours:
            M = cv2.moments(contours)
            if M['m00'] != 0:
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])
            
            if (cX != None or cY != None):
                cv2.circle(smoothed, (cX, cY), 7, (0, 0, 255))
                
        if cX != None:
            angle = 27*(cX - 320)/320    # Finds angle needed to turn
        else:
            angle = 'No line detected'
        
        #f = open('coords.txt', 'a')
        #f.write(str(cX) + ',' + str(cY) + '\n')

        #0 = x angle
        #1 = y pos
        if cY != None:
            if cY > 170:
                sys.stdout.write('stop\n')
            else:
                sys.stdout.write(str(angle) + '\n')
            
        else:
            sys.stdout.write(str(angle) + '\n')
        sys.stdout.flush()
        #print(str(angle))
        cv2.imshow('frame', smoothed)
        cv2.imshow('img', frame)
        #cv2.imshow('thresh', thresh)
                                  
        if cv2.waitKey(1) == ord('q'):
            break
        
    cv2.destroyAllWindows()
    #return(angle)
