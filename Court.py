import cv2
import numpy as np
import imutils

def drawCourt(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([52, 0, 55]), np.array([104, 255, 255]))
    contour = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(contour)
    largest = -1
    for c in cnts:
        if(cv2.contourArea(c) > largest):
            largest = cv2.contourArea(c)
            contour = c
    
    epsilon = 0.01*cv2.arcLength(contour,True)
    approx = cv2.approxPolyDP(contour,epsilon,True)
    y_min = approx.min(axis=0)[0][1]
    y_max = approx.max(axis=0)[0][1]

    for i in range(30,0,-1):
        boundary = i
        temp_corners = []
        for c in approx:

            if c[0][1] <= y_min + boundary or  c[0][1] >= y_max - boundary:
                temp_corners.append(c)

        corners = temp_corners
        if (len(corners) >= 4):
            break
    corners = np.array(corners)

    height, width, channels = image.shape
    otherImage = np.zeros((height,width,channels), np.uint8)
    image = cv2.polylines(image, corners, True, (0,255,0), 5, cv2.LINE_AA)
    cv2.drawContours(image, [corners], -1, (0,255,0), 3)
    cv2.fillPoly(otherImage, pts =[corners], color=(0,255,0))

    return image, otherImage

image = cv2.imread("b3.jpg")
image, otherImage = drawCourt(image)
height, width, channels = image.shape
newImage = np.zeros((2*height,width,channels), np.uint8)
# image = np.zeros((height,width,channels), np.uint8)
newImage[0:otherImage.shape[0], 0:otherImage.shape[1]] = otherImage
newImage[otherImage.shape[0]:, 0:otherImage.shape[1]] = image
cv2.imshow("hi", image)
cv2.waitKey(0)
cv2.imshow("hi", otherImage)
cv2.waitKey(0)
cv2.imshow("hi", newImage)
cv2.waitKey(0)
