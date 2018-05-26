"Class that detects a blue led on the screen and sends it coordinates "
"over USB-port"

import cv2
import numpy as np
import Calibrater
import Serial
assert float(cv2.__version__.rsplit('.', 1)[0]) >= 3

ser = Serial.Serial('COM9', 115200) #initiate the serial communication
img_size = (400,400)
img_draw = np.ones(img_size) * 255
oldCoordinateX = 0
oldCoordinateY = 0

"Returns the clicked pixel on the image"
def find_pixels(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        print("X:" ,x, "Y:",y)
        global xCoordinate
        global yCoordinate
        xCoordinate = x
        yCoordinate = y
"Correction for the height of camera, "
def heighCorrection2(x, y, ledheight, cameraheight, xStart, ystart, offset):
    t = (cameraheight - ledheight)/cameraheight
    vx = x - 200
    vy = 400 - y - offset
    xreal = xStart + t*vx
    yreal = ystart + t*vy
    return [xreal, yreal]

cv2.namedWindow('image')
cv2.setMouseCallback('image', find_pixels)

#lower_blue = np.array([110,125,110]) #gränser utan filter, fungerade sämre i niagara
#upper_blue = np.array([145,255,255])

kernel = np.ones((2,2), np.uint8)

#opens the camera stream, camera hardcoded in router as 192.168.1.10
cap = cv2.VideoCapture("http://root:pass@192.168.1.10/mjpg/video.mjpg")
cap.open("http://root:pass@192.168.1.10/mjpg/video.mjpg")


#recieves the map for calibration on camera
map = Calibrater.calibrateFisheye()


pts_dst = np.array([
    np.array([[0.0], [0.0]]),
    np.array([[400], [0.0]]),
    np.array([[400], [400]]),
    np.array([[0.0], [400]])])

    #p1 = (216, 107)
    #p2 = (584, 109)
    #p3 = (774, 398)
    #p4 = (11, 400)

#demodag niagara
p1 = (213, 53)
p2 = (588, 53)
p3 = (768, 344)
p4 = (37, 343)


pts_corners = np.array([
        np.array([p1]),
        np.array([p2]),
        np.array([p3]),
        np.array([p4])])

# Calculate homography
h, status = cv2.findHomography(pts_corners, pts_dst)
#RoiDimension = 50

while(cap.isOpened()):
    #timer1 = cv2.getTickCount() #used to calculate how long it takes
    ret, img = cap.read()
    #img = ROI.getROI(img, (400, 149), RoiDimension)
    if ret == True:
        img = Calibrater.remapper(img, map[0], map[1]) #remaps the image-removes the distortion
        hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        ##
        #img_blur = cv2.inRange(hsv_image, lower_blue, upper_blue)
        #img_blur = cv2.erode(img_blur, kernel, iterations=2)
        #img_blur = cv2.dilate(img_blur, kernel, iterations=3)
        ##

        #lower_range = np.array([115, 110, 160], np.uint8)
        #upper_range = np.array([145, 255, 255], np.uint8)

        lower_range = np.array([115, 110, 160], np.uint8)
        upper_range = np.array([145, 255, 255], np.uint8)

        # Filters out everything else that is not blue
        mask = cv2.inRange(hsv_image, lower_range, upper_range)
        res = cv2.bitwise_and(img, img, mask=mask)
        x, y, w, height = cv2.boundingRect(mask)
        cv2.rectangle(img, (x, y), (x + w, y + height), (0, 255, 0), 1)
        #print(x+(w/2), y)
        if (w < 1) | (w > 55) | (height > 55): #if rectangle is to big or small we have bad result
            print("bad result", w, height)
            xCoordinate = 255*2
            yCoordinate = 255*2
            realCoordinates = (xCoordinate, yCoordinate)
            #ser.sendData(20, 20) #debugg purposes
        else:
            print("blue found!", w, height)
            xPixel = x + (w/2)
            yPixel = y + (height/1.8)
            point_center = np.array([[xPixel], [yPixel], [1]])
            position = np.matmul(h, point_center)
            xCoordinate = position[0] / position[2] # remove scaling issues
            yCoordinate = position[1] / position[2]
            #print(xCoordinate)
            #print(yCoordinate)
            realCoordinates = heighCorrection2(xCoordinate, yCoordinate, 42, 218, 200, 0, 37) #correction for height

            realYCoordinate = realCoordinates[1]
            realXCoordinate = realCoordinates[0]
            if(realYCoordinate > 380): #correction for accuracy in depth
                realYCoordinate += 8
            elif(realYCoordinate > 370):
                realYCoordinate += 6
            elif(realYCoordinate > 365):
                realYCoordinate += 5
            elif(realYCoordinate > 355):
                realYCoordinate += 4

            print("X:", realXCoordinate, "\n", "Y:",realYCoordinate)
            cv2.line(img_draw, (oldCoordinateX, 400 - oldCoordinateY),
                     (realXCoordinate, 400 - realYCoordinate), (0, 255, 0), 1)#draw the pixels on a white img
            oldCoordinateX = realXCoordinate
            oldCoordinateY = realYCoordinate
            ser.sendData(int(realXCoordinate), int(realYCoordinate)) #sends the coordinate over USB

        cv2.imshow('image2', mask)
        cv2.imshow('image', img)
        cv2.imshow('drawing image', img_draw)
        #ser.sendData(int(realCoordinates[0]), int(realCoordinates[1]))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
