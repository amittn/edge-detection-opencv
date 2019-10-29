# import the necessary packages
from transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="Path to the image to be scanned")
args = vars(ap.parse_args())
# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height=500)

# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 50, 200)
#test8 works with rounded edges its value is  50, 200
#test1 = 0, 75
#test4,test5,test6,test7 = 10,150
##############
# print("STEP 1: Edge Detection")
# cv2.imshow("Image", image)
cv2.imshow("Edged", edged)
key = cv2.waitKey(0)


# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#cv.drawContours(img,[box],0,(0,0,255),2)

print("------1--------")
#print(cnts)
cnts = imutils.grab_contours(cnts)
print("------2--------")
#print(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
print("------3--------")
#print(cnts)
screenCnt = None
w = 0
h = 0

#loop over the contours
for c in cnts:
    #approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    print("------4--------")

    #if our approximated contour has four points, then we
    #can assume that we have found our screen
    if len(approx) == 4:
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)
        shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
        print("inside loop..........")
        print(shape)
        print('---------area is-----------')
        print(w)
        print(h)
        print(w * h)
        screenCnt = approx
        print(screenCnt)
        break


# show the contour (outline) of the piece of paper
print("STEP 2: Find contours............")
print(screenCnt)

# We have to check on the ratio but for now just using area
if (w * h) >= 33953:
    print('------------+++++++1++++++++--------------------')
    print('This is a big rectangle')
else:
    print('------------+++++++2++++++++--------------------')
    print('This is small rectangle')

if screenCnt is None:
    cv2.imshow("Outline", image)
else:
    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
    cv2.imshow("Outline", image)


key = cv2.waitKey(0)

if (key == 113 or key == 27):
    # exit is q or ESC is pressed
    cv2.destroyAllWindows()
    exit()

