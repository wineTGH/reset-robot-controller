from trajectories.base import Trajectory
import arduino

class FirstBoxesToFinish(Trajectory):
    def __init__(self, camera):
        super().__init__(camera)

    def run(self):
        self.drive_to_marker(4, 25_000, True)
        arduino.write("MY:-180;")
        self.drive_to_marker(2, 15_500, ranges=(410, 420))
        