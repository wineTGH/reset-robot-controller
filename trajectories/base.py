from camera import Camera
from arduino import arduino

class Trajectory:
    def __init__(self, camera: Camera, camera_qr: Camera = None, camera_grab: Camera = None):
        self.camera = camera
        self.camera_qr = camera_qr
        self.camera_grab = camera_grab

    def run(self):
        pass

    def drive_to_marker(self, target_marker_id: int, target_area: int, reverse: bool = False, ranges: tuple[int, int] = (250, 350), camera: Camera = None):
        if not camera:
            camera = self.camera
        
        while True:
            if arduino.ser.in_waiting:
                print(arduino.ser.read())

            _, id, x, area = camera.read_marker(target_marker_id)

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