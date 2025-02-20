from trajectories.base import Trajectory
import arduino

class StartToCenterTrajectory(Trajectory):
    def __init__(self, camera):
        super().__init__(camera)

    def run(self):
        self.__drive_to_marker(3, 60_000)

        arduino.write("CY:-90;")

        self.__drive_to_marker(1, 60_000)

        arduino.write("CY:-180;")

        self.__drive_to_marker(2, 1_000, True, ranges=(230, 245))



    def __drive_to_marker(self, target_marker_id: int, target_area: int, reverse: bool = False, ranges: tuple[int, int] = (250, 350)):
        while True:
            _, id, x, area = self.camera.read_marker(target_marker_id)

            if id is None:
                continue

            if id != target_marker_id:
                continue

            if (area >= target_area and not reverse) or (area <= target_area and reverse):
                arduino.write("CS:0;")
                return

            if x < ranges[0]:
                arduino.write("CL:50;")
            elif x > ranges[1]:
                arduino.write("CR:50;")
            else:
                arduino.write("CF:100;") if not reverse else arduino.write("CB:100;")