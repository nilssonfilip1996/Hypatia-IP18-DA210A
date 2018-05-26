import time

import cv2
import numpy as np
from cv2 import imshow
import requests

if __name__ == '__main__':
    print('Posioning starting')


    # Connect to 2 video Sources
    cam1 = cv2.VideoCapture()
    cam2 = cv2.VideoCapture()


    # Open connection with 2 AXIS-cameras
    cam1.open("http://root:pass@192.168.1.3/mjpg/video.mjpg")
    cam2.open("http://root:pass@192.168.1.4/mjpg/video.mjpg")


    # Announce information about connection
    if cam1.isOpened():
        print("Camera 1 connection established.")
    else:
        print("Failed to connect to the camera 1.")
        exit(-1)

    if cam2.isOpened():
        print("Camera 2 connection established.")
    else:
        print("Failed to connect to the camera 2.")
        exit(-1)

    # Grab frames
    while(True):
        ret1,frame1 = cam1.read()
        ret2,frame2 = cam2.read()

        # Convert BGR to HSV
        hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)

        lower_range = np.array([110, 180, 190], np.uint8)
        upper_range = np.array([255, 255, 255], np.uint8)


        # Threshold the HSV image to get only blue colors
        mask1 = cv2.inRange(hsv1, lower_range, upper_range)
        mask2 = cv2.inRange(hsv2, lower_range, upper_range)

        res1 = cv2.bitwise_and(frame1, frame1, mask=mask1)
        res2 = cv2.bitwise_and(frame2, frame2, mask=mask2)

        cv2.imshow('frame1', frame1)
        cv2.imshow('mask1', mask1)
        cv2.imshow('res1', res1)

        cv2.imshow('frame2', frame2)
        cv2.imshow('mask2', mask2)
        cv2.imshow('res2', res2)


        # Find the blue dot and print out the x&y coordinates
        #####################################################
        #
        # distance camera 210 cm
        x1, y1, w1, h1 = cv2.boundingRect(mask1)
        cv2.rectangle(mask1, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 1)
        x2 = x1 + (w1 / 2)
        y2 = (y1 + (h1 / 2))
        print('x1 ', x1, 'y1 ',  y1)
        time.sleep(0.5)



        # Camera 2 calculation
        # distance camera 180 cm
        # The X-coordinates representes Y-coordinate since the
        # X-coordinate from Camera 1 represents the X
        x2, y2, w2, h2 = cv2.boundingRect(mask2)
        cv2.rectangle(mask2, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 1)
        x2 = x2 + (w2 / 2)
        y2 = (y2 + (h2 / 2))
        print('x2 ', x2, 'y2 ',  y2)
        time.sleep(0.5)

        if ((y2 < 355) & (y2 > 288)):
            if ((x2 > 25) & (x2 < 171)):
                x2 = (x2 - 14) * 0.69
            if ((x2 > 170) & (x2 < 393)):
                # 393-26
                x2 = (x2 - 14) * 0.54
            if ((x2 > 392) & (x2 < 627)):
                # 627-26
                x2 = (x2 - 14) * 0.5
            if ((x2 > 625) & (x2 < 789)):
                # 788-26
                x2 = (x2 - 14) * 0.52

        elif ((y2 < 289) & (y2 > 200)):
            if ((x2 > 48) & (x2 < 209)):
                x2 = (x2 - 49) * 0.63
            if ((x2 > 208) & (x2 < 397)):
                x2 = (x2 - 49) * 0.57
            if ((x2 > 396) & (x2 < 595)):
                x2 = (x2 - 49) * 0.55
            if ((x2 > 594) & (x2 < 800)):
                x2 = (x2 - 49) * 0.58

        elif ((y2 < 201) & (y2 > 167)):
            if ((x2 > 91) & (x2 < 231)):
                x2 = (x2 - 91) * 0.71
            if ((x2 > 230) & (x2 < 401)):
                x2 = (x2 - 91) * 0.7
            if ((x2 > 400) & (x2 < 575)):
                x2 = (x2 - 91) * 0.62
            if ((x2 > 574) & (x2 < 721)):
                x2 = (x2 - 91) * 0.63
        elif ((y2 < 168) & (y2 > 130)):
            if ((x2 > 149) & (x2 < 270)):
                x2 = (x2 - 150) * 0.83
            if ((x2 > 269) & (x2 < 402)):
                x2 = (x2 - 150) * 0.8
            if ((x2 > 401) & (x2 < 544)):
                x2 = (x2 - 150) * 0.76
            if ((x2 > 543) & (x2 < 721)):
                x2 = (x2 - 150) * 0.75


        x = x1
        y = x2
        print('distance y', y)
        print('finish loop')
        ##############################################################

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #time.sleep(1)
# When everything done, release the capture
cam1.release()
cam2.release()
cv2.destroyAllWindows()