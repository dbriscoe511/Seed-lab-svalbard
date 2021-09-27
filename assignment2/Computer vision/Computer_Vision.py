from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

camera = PiCamera()

#calibration
camera.start_preview()
sleep(2)

camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_mode = 'off'
camera.awb_gains = g
camera.capture_sequence(['image%02d.png' % i for i in range(10)])
camera.stop_preview()






#Takes a picture and stores to file
fileName = 'test.png'
camera.start_preview()
sleep(5)
camera.capture(fileName)
camera.stop_preview()

kernel = np.ones((5,5),np.uint8)
img = cv.imread(fileName)

hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
#Isolates yellow
lower = np.array([15, 100, 100])
upper = np.array([50, 255, 255])
mask = cv.inRange(hsv, lower, upper)
res = cv.bitwise_and(img, img, mask = mask)
#Cleans up image
closed = cv.morphologyEx(res, cv.MORPH_CLOSE, kernel)
smoothed = cv.medianBlur(closed,5)
#Finds center in the x direction
gray = cv.cvtColor(smoothed,cv.COLOR_BGR2GRAY)
binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY)[1]
ret, thresh = cv.threshold(binary,127,255,0)
_, contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

cnt = contours[0]
M = cv.moments(cnt)
cx = int(M['m10']/M['m00'])
#Finds distance between object center and image center
dis = abs(img.shape[1]/2-cx)
leastDis = min(dis, cx)
fov = 53.5
anglePerPix = fov / img.shape[1]
#Used the 2 centers and field of view per pixel to find the angle between the object and camera
angle = anglePerPix * dis
print("Angle is: " + str(angle))
