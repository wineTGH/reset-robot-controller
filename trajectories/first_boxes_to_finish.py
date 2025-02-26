from trajectories.base import Trajectory
from arduino import arduino, servo
import time
import state

class FirstBoxesToFinish(Trajectory):
    def run(self):
        self.drive_to_marker(4, 2_700, True, ranges=(280, 289))
        self.drive_to_marker(4, 1_380, True, ranges=(260, 270))

        
        arduino.write("PN:0;")
        arduino.write("MY:-180;")
        
        self.drive_to_marker(2, 60_000, ranges=(280, 290))
        self.drive_to_marker(2, 110_500)

        servo.write("PF;")
        time.sleep(2)
        servo.write("PO;")

        if state.boxes == "right":
            arduino.write("MY:160;")
            servo.write("PF;")
            time.sleep(2)
            servo.write("GO;")
            time.sleep(1)
            servo.write("GC;")
            time.sleep(2)
            servo.write("PB;")
            time.sleep(2)
            arduino.write("MY:-180;")

        elif state.boxes == "left":
            arduino.write("MY:-160;")
            servo.write("PF;")
            time.sleep(2)
            servo.write("GO;")
            time.sleep(1)
            servo.write("GC;")
            time.sleep(2)
            servo.write("PB;")
            time.sleep(2)
            arduino.write("MY:-180;")
            
        else:
            servo.write("PF;")
            time.sleep(2)
            servo.write("GO;")
            time.sleep(1)
            servo.write("GC;")
            time.sleep(2)
            servo.write("PB;")
            