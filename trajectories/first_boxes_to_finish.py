from trajectories.base import Trajectory
from arduino import arduino, servo
import time

class FirstBoxesToFinish(Trajectory):
    def run(self):
        time.sleep(0.1)
        
        self.drive_to_marker(4, 2_700, True, ranges=(280, 289))
        self.drive_to_marker(4, 1_380, True, ranges=(260, 270))

        self.drive_to_marker(2, 60_000, ranges=(280, 290), camera=self.camera_grab)
        
        arduino.write("PN:0;")
        arduino.write("MY:-180;")
        
        self.drive_to_marker(2, 110_500)

        servo.write("PF;")
        time.sleep(2)
        servo.write("PO;")