# Louay Khalil

import time
import cv2
import numpy as np
from cv2 import imshow
import requests

if __name__ == '__main__':

    # Print on console
    print('home camera starting')
    print('....................')

    # Connect to video Source
    cam = cv2.VideoCapture()

    # IP-address and username and password needed
    cam.open("http://root:pass@192.168.1.10/mjpg/video.mjpg")

    # Print on console information about camera connection
    if cam.isOpened():
        print("Camera connection established.")
    else:
        print("Failed to connect to the camera .")
        exit(-1)

    # Grab frames
    while (True):
        # Get the video stream
        ret, frame = cam.read()

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Filter settings for RED, GREEN and BLUE
        lower_range = np.array([110, 210, 210], np.uint8)
        upper_range = np.array([180, 255, 255], np.uint8)

        # Threshold the HSV image to get only blue colors
        # Filters out everything else that is not blue
        mask = cv2.inRange(hsv, lower_range, upper_range)

        # Black for empty space and white for the blue area
        res = cv2.bitwise_and(frame, frame, mask=mask)

        # Window-frame to play video stream from differnet streams
        cv2.imshow('frame', frame)
        #cv2.imshow('mask2', mask)
        cv2.imshow('res2', res)


        # Getting the X and Y of the blue area
        x, y, w, h = cv2.boundingRect(mask)
        # cv2.rectangle(mask, (x2, y2), (x2 + w2, y2 + h2), (255, 255, 255), 1)
        x = x + (w / 2)
        y = (y + (h / 2))
        print('x ', x, 'y ', y)

        # Delay of 0.5 sec to slow down
        #time.sleep(0.5)

        ##############################################################

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # time.sleep(1)
# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()