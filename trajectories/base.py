from camera import Camera
import arduino

class Trajectory:
    def __init__(self, camera: Camera):
        self.camera = camera

    def run(self):
        pass


    def drive_to_marker(self, target_marker_id: int, target_area: int, reverse: bool = False, ranges: tuple[int, int] = (250, 350)):
        while True:
            if arduino.ser.in_waiting:
                print(arduino.ser.read())

            _, id, x, area = self.camera.read_marker(target_marker_id)

            if id is None:
                continue

            if id != target_marker_id:
                continue

            if (area >= target_area and not reverse) or (area <= target_area and reverse):
                arduino.write("MS:0;")
                return

            if x < ranges[0]:
                arduino.write("ML:50;")
            elif x > ranges[1]:
                arduino.write("MR:50;")
            else:
                arduino.write("MF:50;") if not reverse else arduino.write("MB:50;")