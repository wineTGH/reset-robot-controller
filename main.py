import cv2 as cv
from camera import Camera
import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)
camera = Camera(2)

prev_command = "CS:0;"
count = 0

while True:
    command = "CS:0;"    
    image, id, x, area = camera.read_marker()

    if id is None:
        cv.imshow("Frame", image)
        continue
    
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
        print(id)
        ser.write((command).encode())
    
    prev_command = command

    cv.imshow("Frame", image)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv.destroyAllWindows()