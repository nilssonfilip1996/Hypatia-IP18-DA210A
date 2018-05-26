# Louay
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



    # Inside Network
    # Home is fifteen always with a zero starts with 192.168.0.15

    cam.open("http://root:pass@192.168.1.10/mjpg/video.mjpg")
    # Outside Network



    if cam.isOpened():
        print("Camera connection established.")
    else:
        print("Failed to connect to the camera .")
        exit(-1)


    # Grab frames
    while(True):
        ret,frame = cam.read()
        #cv2.imshow('frame2', frame)


        # Crop code here

        x1 = 233
        x2 = 575
        x3 = 84
        x4 = 727
        y1 = 70
        y2 = 353

        # original image
        # -1 loads as-is so if it will be 3 or 4 channel as the original
        image = frame
        maskk = np.zeros(image.shape, dtype=np.uint8)
        roi_corners = np.array([[(x1, y1), (x3, y2),(x4, y2), (x2, y1)]], dtype=np.int32)

        # fill the ROI so it doesn't get wiped out when the mask is applied
        channel_count = image.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
        cv2.fillPoly(maskk, roi_corners, ignore_mask_color)
        # from Masterfool: use cv2.fillConvexPoly if you know it's convex

        # apply the mask
        masked_image = cv2.bitwise_and(image, maskk)
        newX = 0
        newY = 0
        str1 = (" X: " + str(newX) + " Y: " + str(newY))

        cv2.putText(masked_image, 'HYPATIA', (224, 65), cv2.FONT_HERSHEY_DUPLEX, 2.8, 255)
        cv2.putText(masked_image, 'MAU - 2018', (24, 500), cv2.FONT_HERSHEY_DUPLEX, 3.8, 255)
        cv2.putText(masked_image, str1, (0, 590), cv2.FONT_HERSHEY_DUPLEX, 3.2, 255)
        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        # save the result
        cv2.imshow("window", masked_image)

        # Crop code ends


        # Convert BGR to HSV
        hsv = cv2.cvtColor(masked_image, cv2.COLOR_BGR2HSV)


        lower_range = np.array([110, 230, 230], np.uint8)
        upper_range = np.array([130, 255, 255], np.uint8)


        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_range, upper_range)


        res = cv2.bitwise_and(image, masked_image, mask=mask)

        ##############################################################

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #time.sleep(1)
# When everything done, release the capture
cam.release()

cv2.destroyAllWindows()