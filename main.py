import UdpComms as U
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import time
import os

'''
This programs uses UdpComms.py from Siliconifier's github repository: https://github.com/Siliconifier/Python-Unity-Socket-Communication
'''

#Initializes the pong game
os.startfile("Interactive_Pong\Build\Pong.exe")

# Create UDP socket to use for sending (and receiving)
sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)
i = 0
dataArray = [25, 25]
final = "000000"

#Video Start
LeftCamera = cv.VideoCapture(0, cv.CAP_DSHOW)
RightCamera = cv.VideoCapture(0, cv.CAP_DSHOW)

lower = 140
upper = 255

def bright_feed(capture, capturename):
    #bright setup
    print("Press S to save the bright image. Everyone should have their lights turned ON and faced towards the camera!")
    #waiting loop for saved bright image
    while True:
        isTrue, frame = capture.read()
        cam = cv.flip(frame, 1)
        Feed = calc_simple(cam)
        cv.imshow("Feed", Feed)
        if ( cv.waitKey(5) & 0xFF==ord("s") ):
            cv.imwrite(("Interactive Design Project\Project\{}.jpg".format(capturename)), cam)
            break

    #saved bright image
    bright = cv.imread("Interactive Design Project\Project\{}.jpg".format(capturename))
    cv.destroyWindow("Feed")
    cv.imshow("Bright", bright)
    time.sleep(0.5)
    cv.destroyWindow("Bright")
    return bright

def dark_feed(capture, capturename):
    #dark setup
    print("Press S to save the dark image. Everyone should have their lights turned OFF!")
    #waiting loop for saved dark image
    while True:
        isTrue, frame = capture.read()
        cam = cv.flip(frame, 1)
        Feed = calc_simple(cam)
        cv.imshow("Feed", Feed)
        if ( cv.waitKey(5) & 0xFF==ord("s") ):
            cv.imwrite(("Interactive Design Project\Project\{}.jpg".format(capturename)), cam)
            break

    #saved dark image
    dark = cv.imread("Interactive Design Project\Project\{}.jpg".format(capturename))
    cv.destroyWindow("Feed")
    cv.imshow("Dark", dark)
    time.sleep(0.5)
    cv.destroyWindow("Dark")
    return dark

def calc(img):
    blurred = cv.GaussianBlur(img, (3, 3), 0)
    #cv.imshow("blurred", blurred)
    dilate_amount = 33
    dilated = cv.dilate(blurred, (dilate_amount, dilate_amount), iterations=3)
    #cv.imshow("dilated", dilated)
    gray = cv.cvtColor(dilated, cv.COLOR_BGR2GRAY)
    #cv.imshow("gray", gray)

    lowerbound = np.array([lower]) 
    upperbound = np.array([upper]) 

    mask = cv.inRange(gray, lowerbound, upperbound)
    #cv.imshow("Black", mask)

    ratio =(cv.countNonZero(mask))/(img.size/3)

    #print("White in image", np.round(ratio*100, 2),"%")

    printedval = (np.round(ratio*100, 2))

    return printedval
    
def calc_simple(img):
    blurred = cv.GaussianBlur(img, (3, 3), 0)
    #cv.imshow("blurred", blurred)
    dilate_amount = 33
    dilated = cv.dilate(blurred, (dilate_amount, dilate_amount), iterations=3)
    #cv.imshow("dilated", dilated)
    gray = cv.cvtColor(dilated, cv.COLOR_BGR2GRAY)
    #cv.imshow("gray", gray)

    lowerbound = np.array([lower]) 
    upperbound = np.array([upper]) 

    mask = cv.inRange(gray, lowerbound, upperbound)
    #cv.imshow("Black", mask)

    ratio =(cv.countNonZero(mask))/(img.size/3)

    #print("White in image", np.round(ratio*100, 2),"%")
    value = (np.round(ratio*100, 2))
    return mask

def variable_assign(bright, dark):
    maxval = bright + (bright*0.10)
    #print("max val", maxval_1)
    minval = dark
    #print("min val", minval_1)

    realmaxval = (maxval - minval)
    return(realmaxval, maxval, minval)

def setup(bright, dark):
    BrightOrigin = calc(bright)
    #print(BrightOrigin)
    DarkOrigin = calc(dark)   
    #print(DarkOrigin)
    realmaxval, maxval, minval = variable_assign(BrightOrigin, DarkOrigin) 



    return realmaxval, maxval, minval

def feed_calc(originalval, minval, realmaxval):
    feedval = (originalval-minval)
    value = ((feedval * 100) // realmaxval)
    #print(value)

    if(value > 100):
        printed_value = 100
    elif(value < 0):
        printed_value = 0
    else:
        printed_value = value

    return printed_value

leftbright = bright_feed(LeftCamera, "Left Bright")
cv.imshow("Left Bright", leftbright)
rightbright = bright_feed(RightCamera, "Right Bright")
cv.imshow("Right Bright", rightbright)
leftdark = dark_feed(LeftCamera, "Left Dark")
cv.imshow("Left Dark", leftdark)
rightdark = dark_feed(RightCamera, "Right Dark")
cv.imshow("Right Dark", rightdark)

LeftRealMaxVal, LeftMaxVal, LeftMinVal = setup(leftbright, leftdark)
RightRealMaxVal, RightMaxVal, RightMinVal= setup(rightbright, rightdark)

print("Starting Values")
print("Left Values", LeftRealMaxVal, LeftMaxVal, LeftMinVal)
print("Right Values", RightRealMaxVal, RightMaxVal, RightMinVal)
#Setup
time.sleep(3)
cv.destroyWindow("Left Bright")
cv.destroyWindow("Right Bright")
cv.destroyWindow("Left Dark")
cv.destroyWindow("Right Dark")

#Video Loop
while True:
#Setup
    print("Updated Values:")
#Left
    #Sets up camera feeds for analysis
    isTrue, frame = LeftCamera.read()
    LeftFeed = cv.flip(frame, 1)

    LeftDisplayFeed = calc_simple(LeftFeed)
    cv.imshow("Left Feed", LeftDisplayFeed)

    LeftOriginalValue = calc(LeftFeed)
    LeftValue = feed_calc(LeftOriginalValue, LeftMinVal, LeftRealMaxVal)

#Right
    #Sets up camera feeds for analysis
    isTrue, frame = RightCamera.read()
    RightFeed = cv.flip(frame, 1)

    RightDisplayFeed = calc_simple(RightFeed)
    cv.imshow("Right Feed", RightDisplayFeed)

    RightOriginalValue = calc(RightFeed)
    RightValue = feed_calc(RightOriginalValue, RightMinVal, RightRealMaxVal)

#Send Stuff
    dataArray[0] = LeftValue
    dataArray[1] = RightValue
    print("Array:")
    print(dataArray)

    data_str = "" 
    for i in dataArray:
        if i < 100:
            data_str += "0"
        if i < 10:
            data_str += "0"
        data_str += str(i)
    #print(data_str)
    sock.SendData(data_str) # Send this string to other application
    i += 1
    data = sock.ReadReceivedData() # read data
    if data != None: # if NEW data has been received since last ReadReceivedData function call
        print(data) # print new received data

#How to Exit Loop
    if ( cv.waitKey(5) & 0xFF==ord("d") ):
        break
    print("")

LeftCamera.release()
RightCamera.release()
print("End")
print("Starting Values")
print("Left Values", LeftRealMaxVal, LeftMaxVal, LeftMinVal)
print("Right Values", RightRealMaxVal, RightMaxVal, RightMinVal)

cv.destroyAllWindows
