from trajectories.base import Trajectory
import arduino
import time

class FirstBoxesToFinish(Trajectory):
    def __init__(self, camera, *args, **kwargs):
        super().__init__(camera, args, kwargs)

    def run(self):
        time.sleep(0.1)
        self.drive_to_marker(4, 2_700, True, ranges=(280, 289))
        self.drive_to_marker(4, 1_380, True, ranges=(260, 270))
        arduino.write("PN:0;")
        arduino.write("MY:-180;")
        self.drive_to_marker(2, 15_500)
