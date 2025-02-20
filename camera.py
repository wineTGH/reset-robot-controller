import cv2 as cv
import cv2.aruco as aruco
from cv2.typing import MatLike
class Camera:

    def __init__(self, id: int):
        self.cap = cv.VideoCapture(id)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

        dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        params = aruco.DetectorParameters()
        self.detector = aruco.ArucoDetector(dictionary, params)

    def release(self):
        self.cap.release()
    
    def read_marker(self) -> tuple[MatLike, int, int, int] | tuple[MatLike, None, None, None]:
        _, self.image = self.cap.read()

        gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        corners, ids, rejected = self.detector.detectMarkers(gray)

        if ids is None:
            self.show_image()
            return self.image, None, None, None
        
        aruco.drawDetectedMarkers(self.image, corners)
        self.show_image()
        
        area = cv.contourArea(corners[0])
        moments = cv.moments(corners[0])

        x = int(moments["m10"]/moments["m00"]) if moments["m00"] != 0 else 320

        return self.image, int(ids[0]), x, area
    
    def show_image(self):
        if self.image is not None:
            cv.imshow("Camera", self.image)

        return cv.waitKey(1) & 0xFF == ord('q')
            
        
    def __del__(self, *args, **kwargs):
        self.cap.release()