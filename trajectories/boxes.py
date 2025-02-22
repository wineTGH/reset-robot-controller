import arduino
from trajectories.base import Trajectory

class BoxesTrajectory(Trajectory):
    def __init__(self, camera):
        super().__init__(camera)

    def run(self):
        self.drive_to_qr_code()

    def drive_to_qr_code(self):
        while True:
            if arduino.ser.in_waiting:
                print(arduino.ser.readline())
            
            image, data, x, area = self.camera.read_qr()

            if not data or data != "прокладки":
                arduino.write("MF:20;")
                continue

            arduino.write("MS:0;")
            break
            # TODO: GRAB


    