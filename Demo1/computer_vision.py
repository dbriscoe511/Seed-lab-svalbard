from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep
import numpy as np
import cv2
import io
import sys

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30

gains = []
camera.start_preview()
sleep(3)
camera.stop_preview()
for i in range(0, 10):
    gains.append(camera.awb_gains)

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
    lower = np.array([70, 50, 50])
    upper = np.array([130, 255, 255])
    
    mask = cv2.inRange(hsv, lower, upper)
    results = cv2.bitwise_and(frame, frame, mask=mask)
    
    kernel = np.ones((5,5),np.uint8)
    closed = cv2.morphologyEx(results, cv2.MORPH_CLOSE, kernel)
    smoothed = cv2.medianBlur(closed,5)
    
    grayscale = cv2.cvtColor(smoothed, cv2.COLOR_BGR2GRAY)     # Converts to grayscale
    
    ret,thresh = cv2.threshold(grayscale,50,255,cv2.THRESH_BINARY)   # Performs thresholding
    
    arr = np.array(thresh)       # Converts threshold to numPy
    arr = np.nonzero(arr)        # Nonzeros the numPy array
    locateX = np.mean(arr[1])    # Finds center of marker
    locateY = np.mean(arr[0])
    
    angle = 27*(locateX - 320)/320    # Finds angle needed to turn
    
    sys.stdout.write(str(angle) + '\n')
    
    cv2.imshow('frame', thresh)
                              
    if cv2.waitKey(1) == ord('q'):
        break
    
cv2.destroyAllWindows()