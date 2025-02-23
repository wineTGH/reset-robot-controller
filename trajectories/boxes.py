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
        count = 0
        while True:
            image, data, x, area = self.camera_qr.read_qr()

            if not data:
                arduino.write("MF:20;")
                continue

            arduino.write("MS:0;")

            arduino.write("PG:500;")
            
            while True:
                _, data, _, _ = self.camera_grab.read_qr()
                if data:
                    break
            
            arduino.write("PA:1;")
            time.sleep(10)
            
            arduino.write("PP:1;")
            time.sleep(20)
            arduino.write("PG:200;")
            time.sleep(4)
            servo.write("GO;")
            time.sleep(2)
            
            servo.write("PF;")
            time.sleep(2)
            
            servo.write("GC;")
            time.sleep(1)
            
            servo.write("PB;")

            time.sleep(2)
            arduino.write("PA:0;")
            arduino.write("PP:-1;")
            time.sleep(15)

            return