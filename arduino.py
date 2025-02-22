import serial
import time
ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)

previous_command = "CS:0;"

def write(command: str):
    global previous_command
    
    if command != previous_command:
        ser.write(command.encode())
        print(command)

    previous_command = command

