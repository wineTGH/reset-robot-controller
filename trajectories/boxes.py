from arduino import arduino, servo
import time
from trajectories.base import Trajectory

class BoxesTrajectory(Trajectory):
    def __init__(self, camera, camera_qr, camera_grab):
        if not camera_grab or not camera_qr:
            raise FileNotFoundError("не найдены камеры захвата и qr")
        
        super().__init__(camera, camera_qr, camera_grab)

    def run(self):
        arduino.write("PG:140;")
        time.sleep(1)
        self.drive_to_qr_code()

    def drive_to_qr_code(self):
        while True:
            _, data, _, _ = self.camera_qr.read_qr()

            if not data:
                arduino.write("MF:20;")
                continue

            arduino.write("MS:0;")
            self.grab_lower_part()

            arduino.write("PG:500;")
            time.sleep(4)
            
            _, data, _, _ = self.camera_grab.read_qr()
            self.grab_higher_part()
        
    def grab_lower_part(self):
        arduino.write("PG:140;")
        servo.write("GO;")
        time.sleep(2)
        servo.write("PF;")
        time.sleep(3)
        servo.write("GC;")
    
    def grab_higher_part(self):
        arduino.write("PP:1;")
        time.sleep(16)
        arduino.write("PG:430;")
        time.sleep(4)
        servo.write("GO;")
        time.sleep(2)
        servo.write("PF;")
        time.sleep(5)
        servo.write("GC;")
        arduino.write("PA:1;")
        time.sleep(10)
        servo.write("PB;")
        arduino.write("PA:0;")