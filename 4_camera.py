import UdpComms as U
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import time
import os
import argparse

'''
This programs uses UdpComms.py from Siliconifier's github repository: https://github.com/Siliconifier/Python-Unity-Socket-Communication
'''

#Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--save_video", default = False, type = bool, help = "True or False to save video of all camera feed")
parser.add_argument("--fps", default = 30, type = int, help = "Set FPS of all cameras")
parser.add_argument("--width", default = 1280, type = int, help = "Set width for cameras")
parser.add_argument("--height", default = 720, type = int, help = "Set height for cameras")
parser.add_argument("--light_range", default = [140, 255], nargs = "+", help = "List with 2 values between 0-255 (a low threshold and high threshold) on grayscale. Anything between these 2 values will be counted as light.")
args = parser.parse_args()

#Initializes the pong game
os.startfile("Interactive_Pong\Build\Pong.exe")

# Create UDP socket to use for sending (and receiving)
sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)
i = 0
dataArray = [25, 25]
final = "000000"

#Video Start
LeftCamera1 = cv.VideoCapture(0, cv.CAP_DSHOW)
LeftCamera1.set(cv.CAP_PROP_FPS, args.fps)
LeftCamera1.set(cv.CAP_PROP_FRAME_WIDTH, args.width)
LeftCamera1.set(cv.CAP_PROP_FRAME_HEIGHT, args.height)

LeftCamera2 = cv.VideoCapture(1, cv.CAP_DSHOW)
LeftCamera2.set(cv.CAP_PROP_FPS, args.fps)
LeftCamera2.set(cv.CAP_PROP_FRAME_WIDTH, args.width)
LeftCamera2.set(cv.CAP_PROP_FRAME_HEIGHT, args.height)

RightCamera1 = cv.VideoCapture(2, cv.CAP_DSHOW)
RightCamera1.set(cv.CAP_PROP_FPS, args.fps)
RightCamera1.set(cv.CAP_PROP_FRAME_WIDTH, args.width)
RightCamera1.set(cv.CAP_PROP_FRAME_HEIGHT, args.height)

RightCamera2 = cv.VideoCapture(3, cv.CAP_DSHOW)
RightCamera2.set(cv.CAP_PROP_FPS, args.fps)
RightCamera2.set(cv.CAP_PROP_FRAME_WIDTH, args.width)
RightCamera2.set(cv.CAP_PROP_FRAME_HEIGHT, args.height)

lower = int(args.light_range[0])
upper = int(args.light_range[1])

#Create necessary folders
if not os.path.exists("media"):
    os.makedirs("media")
if not os.path.exists("media/videos"):
    os.makedirs("media/videos")
if not os.path.exists("media/callibration_photo"):
    os.makedirs("media/callibration_photo")


def callibration(capture, capturename, bright):
    #bright setup
    if bright:
        print("Press S to save the bright image. Everyone should have their lights turned ON and faced towards the camera!")
    if not bright:  
        print("Press S to save the dark image. Everyone should have their lights turned OFF!")

    #waiting loop for saved callibration image
    while True:
        isTrue, frame = capture.read()
        frame = cv.resize(frame,(args.width, args.height), interpolation = cv.INTER_CUBIC) 
        cam = cv.flip(frame, 1)
        Feed = calc_simple(cam)
        cv.imshow("Feed", Feed)
        if ( cv.waitKey(5) & 0xFF==ord("s") ):
            cv.imwrite(("media/callibration_photo/{}.jpg".format(capturename)), cam)
            break

    #saved bright image
    callibration_image = cv.imread("media/callibration_photo/{}.jpg".format(capturename))
    cv.destroyWindow("Feed")
    if bright: 
        cv.imshow("Bright", callibration_image)
    if not bright:
        cv.imshow("Dark", callibration_image)
    time.sleep(0.5)
    if bright:
        cv.destroyWindow("Bright")
    if not bright:
        cv.destroyWindow("Dark")
    return callibration_image

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

#Bright Callibration Image
leftbright1 = callibration(LeftCamera1, "Left_Bright1", True)
cv.imshow("Left Bright", leftbright1)
leftbright2 = callibration(LeftCamera2, "Left_Bright2", True)
cv.imshow("Left Bright", leftbright2)
rightbright1 = callibration(RightCamera1, "Right_Bright1", True)
cv.imshow("Right Bright", rightbright1)
rightbright2 = callibration(RightCamera2, "Right_Bright2", True)
cv.imshow("Right Bright", rightbright2)

#Dark Callibration Image
leftdark1 = callibration(LeftCamera1, "Left_Dark1", False)
cv.imshow("Left Dark", leftdark1)
leftdark2 = callibration(LeftCamera2, "Left_Dark2", False)
cv.imshow("Left Dark", leftdark2)
rightdark1 = callibration(RightCamera1, "Right_Dark1", False)
cv.imshow("Right Dark", rightdark1)
rightdark2 = callibration(RightCamera2, "Right_Dark2", False)
cv.imshow("Right Dark", rightdark2)

LeftVal_1, LeftMaxVal_1, LeftMinVal_1 = setup(leftbright1, leftdark1)
LeftVal_2, LeftMaxVal_2, LeftMinVal_2 = setup(leftbright2, leftdark2)
RightVal_1, RightMaxVal_1, RightMinVal_1= setup(rightbright1, rightdark1)
RightVal_2, RightMaxVal_2, RightMinVal_2= setup(rightbright2, rightdark2)

print("Starting Values")
print("Left Values 1", LeftVal_1, LeftMaxVal_1, LeftMinVal_1)
print("Left Values 2", LeftVal_2, LeftMaxVal_2, LeftMinVal_2)
print("Right Values 1", RightVal_1, RightMaxVal_1, RightMinVal_1)
print("Right Values 2", RightVal_2, RightMaxVal_2, RightMinVal_2)
#Setup
time.sleep(3)
cv.destroyAllWindows()

if args.save_video:
    fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')
    vid_number = os.listdir("media/videos/")
    out = cv.VideoWriter(f"media/videos/recorded_video_{len(vid_number)}.mp4", fourcc, args.fps/4, (args.width * 2, args.height * 2))

#Video Loop
while True:
    print("Updated Values:")
    #Left1
    #Sets up camera feeds for analysis
    isTrue, frame = LeftCamera1.read()
    LeftFeed1 = cv.flip(frame, 1)

    LeftDisplayFeed1 = calc_simple(LeftFeed1)
    cv.imshow("Left Feed 1", LeftDisplayFeed1)

    LeftOriginalValue1 = calc(LeftFeed1)
    LeftValue1 = feed_calc(LeftOriginalValue1, LeftMinVal_1, LeftVal_1)

    #Left2
    #Sets up camera feeds for analysis
    isTrue, frame = LeftCamera2.read()
    LeftFeed2 = cv.flip(frame, 1)

    LeftDisplayFeed2 = calc_simple(LeftFeed2)
    cv.imshow("Left Feed 2", LeftDisplayFeed2)

    LeftOriginalValue2 = calc(LeftFeed2)
    LeftValue2 = feed_calc(LeftOriginalValue2, LeftMinVal_2, LeftVal_2)

    #Right1
    #Sets up camera feeds for analysis
    isTrue, frame = RightCamera1.read()
    RightFeed1 = cv.flip(frame, 1)

    RightDisplayFeed1 = calc_simple(RightFeed1)
    cv.imshow("Right Feed 1", RightDisplayFeed1)

    RightOriginalValue1 = calc(RightFeed1)
    RightValue1 = feed_calc(RightOriginalValue1, RightMinVal_1, RightVal_1)

    #Right 2
    #Sets up camera feeds for analysis
    isTrue, frame = RightCamera2.read()
    RightFeed2 = cv.flip(frame, 1)

    RightDisplayFeed2 = calc_simple(RightFeed2)
    cv.imshow("Right Feed 2", RightDisplayFeed2)

    RightOriginalValue2 = calc(RightFeed2)
    RightValue2 = feed_calc(RightOriginalValue2, RightMinVal_2, RightVal_2)

    LeftValue = ((LeftValue1+LeftValue2)//2)
    RightValue = ((RightValue1+RightValue2)//2)

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
    if ( cv.waitKey(5) & 0xFF==ord("q") ):
        break
    print("")

    if args.save_video:
        combined_feed_left = cv.vconcat([LeftFeed1, LeftFeed2])
        combined_feed_right = cv.vconcat([RightFeed1, RightFeed2])
        combined_feed = cv.hconcat([combined_feed_left, combined_feed_right])
        out.write(combined_feed)

LeftCamera1.release()
LeftCamera2.release()
RightCamera1.release()
RightCamera2.release()
print("End")
print("Starting Values")
print("Left Values 1", LeftVal_1, LeftMaxVal_1, LeftMinVal_1)
print("Left Values 2", LeftVal_2, LeftMaxVal_2, LeftMinVal_2)
print("Right Values 1", RightVal_1, RightMaxVal_1, RightMinVal_1)
print("Right Values 2", RightVal_2, RightMaxVal_2, RightMinVal_2)

if args.save_video:
    out.release()
cv.destroyAllWindows
