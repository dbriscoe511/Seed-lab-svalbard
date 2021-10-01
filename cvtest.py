import cv2 as cv

img = cv.imread('test.png')
width = int(img.shape[1]/2)
height = int(img.shape[0]/2)
newSize = (width, height)
sized = cv.resize(img, newSize, interpolation = cv.INTER_AREA)
cv.imshow('img', sized)
cv.waitKey()
cv.destroyAllWindows()