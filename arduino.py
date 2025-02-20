import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
previous_command = "CS:0;"

def write(command: str):
    global previous_command
    
    if command != previous_command:
        ser.write(command.encode())
        print(command)

    previous_command = command

