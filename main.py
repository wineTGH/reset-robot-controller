import cv2 as cv
import serial
import cv2.aruco as aruco
import numpy as np
import time

ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)
cap = cv.VideoCapture(2)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
params = aruco.DetectorParameters()
detector = aruco.ArucoDetector(dictionary, params)
prev_command = "CS:0;"
count = 0

while True:
    if ser.in_waiting > 0:
        print(ser.read_all())

    ret, image = cap.read()

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    corners, ids, rejected = detector.detectMarkers(gray)
    command = "CS:0;"

    if ids is not None:
        aruco.drawDetectedMarkers(image, corners)
        area = cv.contourArea(corners[0])
        moments = cv.moments(corners[0])


        x = int(moments["m10"]/moments["m00"]) if moments["m00"] != 0 else 320

        if area >= 60_000:
            ser.write(("CY:-90;").encode())
            command = "CS:0;"
        elif x < 250:
            command = "CL:50;"
        elif x > 350:
            command = "CR:50;"
        else:
            command = "CF:100;"
    
    if prev_command != command:
        ser.write((command).encode())
    
    prev_command = command

    cv.imshow("Frame", image)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()