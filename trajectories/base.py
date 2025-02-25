from camera import Camera
from arduino import arduino

class Trajectory:
    def __init__(self, camera: Camera, camera_qr: Camera = None, camera_grab: Camera = None):
        self.camera = camera
        self.camera_qr = camera_qr
        self.camera_grab = camera_grab

    def run(self) -> bool:
        pass

    def drive_to_marker(self, target_marker_id: int, target_area: int, reverse: bool = False, ranges: tuple[int, int] = (250, 350), camera: Camera = None):
        """Функция езды до маркера.

        Args:
            target_marker_id (int): ID маркера, до которого едем
            target_area (int): До какой площади маркера робот едет
            reverse (bool, optional): Езда назад. По-умолчанию False (едем вперёд).
            ranges (tuple[int, int], optional): диапазон отклонения маркера по координате X. По-умолчанию (250, 350).
            camera (Camera, optional): С какой камеры читаем маркер. По умолчанию с той камеры, что указали при создании класса.
        """
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