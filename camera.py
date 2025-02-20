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
    
    def read_marker(self, target_id: int) -> tuple[MatLike, int, int, int] | tuple[MatLike, None, None, None]:
        _, self.image = self.cap.read()

        gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        corners, ids, rejected = self.detector.detectMarkers(gray)

        if ids is None:
            self.show_image()
            return self.image, None, None, None
        
        data_id = self.get_index(ids, target_id)
        if data_id is None:
            self.show_image()
            return self.image, None, None, None
        
        aruco.drawDetectedMarkers(self.image, [corners[data_id]])
        self.show_image()
        
        area = cv.contourArea(corners[data_id])
        moments = cv.moments(corners[data_id])

        x = int(moments["m10"]/moments["m00"]) if moments["m00"] != 0 else 320

        return self.image, int(ids[data_id]), x, area
    
    def show_image(self):
        if self.image is not None:
            cv.imshow("Camera", self.image)

        return cv.waitKey(1) & 0xFF == ord('q')
            
    def get_index(self, ids: MatLike, target_id: int):
        for i in range(len(ids)):
            if int(ids[i]) == target_id:
                return i
        
        return None

    def __del__(self, *args, **kwargs):
        self.cap.release()