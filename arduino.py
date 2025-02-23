import serial
import time

class Arduino:
    previous_command = "CS:0;"
    
    def __init__(self, port: str):
        self.ser = serial.Serial(port, 9600)
        time.sleep(2)


    def write(self, command: str):
        if command != self.previous_command:
            self.ser.write(command.encode())
            print(command)

        self.previous_command = command

arduino = Arduino("/dev/ttyACM0")
servo = Arduino("/dev/ttyACM1")