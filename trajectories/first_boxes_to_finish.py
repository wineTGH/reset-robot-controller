from trajectories.base import Trajectory
import arduino
import time

class FirstBoxesToFinish(Trajectory):
    def __init__(self, camera):
        super().__init__(camera)

    def run(self):
        time.sleep(0.1)
        self.drive_to_marker(4, 2_700, True, ranges=(280, 289))
        arduino.write("MY:-180;")
        self.drive_to_marker(2, 15_500, ranges=(410, 420))
