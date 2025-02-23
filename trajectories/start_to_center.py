from trajectories.base import Trajectory
from arduino import arduino

class StartToCenterTrajectory(Trajectory):
    def __init__(self, camera):
        super().__init__(camera)

    def run(self):
        self.drive_to_marker(3, 60_000)

        arduino.write("MY:-90;")

        self.drive_to_marker(1, 60_000)

        arduino.write("MY:0;")

        self.drive_to_marker(4, 17_000, ranges=(280, 289))