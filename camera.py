import cv2 as cv
import cv2.aruco as aruco
from cv2.typing import MatLike
class Camera:

    def __init__(self, id: int, name: str = "camera"):
        self.name = name
        self.cap = cv.VideoCapture(id)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

        dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        params = aruco.DetectorParameters()
        self.aruco_detector = aruco.ArucoDetector(dictionary, params)
        self.qr_detector = cv.QRCodeDetector()


    def release(self):
        self.cap.release()
    
    def read_marker(self, target_id: int) -> tuple[MatLike, int, int, int] | tuple[MatLike, None, None, None]:
        _, self.image = self.cap.read()

        if self.image is None:
            return None, None, None, None

        gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        corners, ids, rejected = self.aruco_detector.detectMarkers(gray)

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
    
    def read_qr(self, target_data: str = None):
        _, self.image = self.cap.read()
        gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        
        data, points, _ = self.qr_detector.detectAndDecode(gray)

        if not data:
            self.show_image()
            return self.image, None, None, None
        
        if target_data is not None and data != target_data:
            self.show_image()
            return self.image, None, None, None
        
        cv.polylines(self.image, [points.astype(int)], True, (0, 255, 0), 5)
        self.show_image()
        
        area = cv.contourArea(points)
        moments = cv.moments(points)

        x = int(moments["m10"]/moments["m00"]) if moments["m00"] != 0 else 320

        return self.image, data, x, area
    
    def show_image(self):
        if self.image is not None:
            cv.imshow(self.name, self.image)

        return cv.waitKey(1) & 0xFF == ord('q')
            
    def get_index(self, ids: MatLike, target_id: int):
        for i in range(len(ids)):
            if int(ids[i]) == target_id:
                return i
        
        return None

    def __del__(self, *args, **kwargs):
        self.cap.release()