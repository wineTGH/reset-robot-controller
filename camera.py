import cv2 as cv
import cv2.aruco as aruco
from cv2.typing import MatLike


class Camera:
    def __init__(self, id: int | str, name: str = "camera"):
        self.name = name
        self.cap = cv.VideoCapture(id)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

        dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        params = aruco.DetectorParameters()
        self.aruco_detector = aruco.ArucoDetector(dictionary, params)
        self.qr_detector = cv.QRCodeDetector()

    def release(self):
        """выключение камеры"""
        self.cap.release()

    def read_marker(self, target_id: int) -> (
        tuple[None, None, None, None]
        | tuple[MatLike, None, None, None]
        | tuple[MatLike, int, int, int]
    ):
        """
        Фукнция чтение ArUco маркера с текущей камеры

        Аргументы:
        ----------
            - target_id (int): ID искомого маркера. Все маркеры с иными ID игнорируются

        Возвращает:
        ----------
            - image (MatLike | None): изображение с камеры. None если камера не вернула изображение
            - id (int | None): ID искомого маркера. None если маркер не был найден
            - x (int | None): Центр маркера по координате X. None если маркер не был найден
            - area (int | None): Площадь искомого маркера. None если маркер не был найден
        """
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

        x = int(moments["m10"] / moments["m00"]) if moments["m00"] != 0 else 320

        return self.image, int(ids[data_id]), x, area

    def read_qr(
        self, target_data: str = None
    ) -> (
        tuple[None, None, None, None]
        | tuple[MatLike, None, None, None]
        | tuple[MatLike, str, int, int]
    ):
        """
        Фукнция чтение QR кода с текущей камеры
        
        Аргументы:
        ----------
            - target_data (str, optional): Данные на искомом QR-коде. Если аргумент не установлен, программа ищет любой код

        Возвращает:
        ----------
            - image (MatLike | None): изображение с камеры. None если камера не вернула изображение
            - data (str | None): Данные с QR кода. None если код не был найден
            - x (int | None): Центр QR кода по координате X. None если код не был найден
            - area (int | None): Площадь искомого QR кода. None если код не был найден
        """
        _, self.image = self.cap.read()

        if self.image is None:
            return None, None, None, None

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

        x = int(moments["m10"] / moments["m00"]) if moments["m00"] != 0 else 320

        return self.image, data, x, area
    
    def detect_color_area(self, color: dict, min_area: int = 1_000):
        """
        Фукнция чтение цветовой метки
        
        Аргументы:
        ----------
            - color_low (list[int]): Нижняя граница цветов
            - color_high (list[int]): Верхняя граница цветов
            - min_area (list[int], optional): минимальная площадь цветовой метки. Если площадь метки меньше минимального значение, мы её игнорируем. 

        Возвращает:
        ----------
            - image (MatLike | None): изображение с камеры. None если камера не вернула изображение
            - x (int | None): Центр цветовой метки по координате X. None если метка не была найдена
            - area (int | None): Площадь цветовой метки по координате X. None если метка не была найдена
        """
        _, self.image = self.cap.read()

        if self.image is None:
            return None, None, None
        
        g_frame = cv.cvtColor(self.image, cv.COLOR_BGR2LAB)
        g_frame = cv.GaussianBlur(g_frame, (9, 9), 3)
        g_frame = cv.inRange(
            g_frame,
            color['low'],
            color['high'],
        )

        cnt, h = cv.findContours(g_frame, 1, cv.CHAIN_APPROX_SIMPLE)
        if len(cnt) == 0:
            self.show_image()
            return self.image, None, None
        
        cnt = max(cnt, key=cv.contourArea)
        area = cv.contourArea(cnt)
        if area < min_area:
            self.show_image()
            return self.image, None, None
        
        approx = cv.convexHull(cnt)
        rect = cv.minAreaRect(approx)
        box = cv.boxPoints(rect)

        cv.drawContours(self.image, [box.astype(int)], 0, (0, 0, 255), 2)
        cv.drawContours(self.image, [approx.astype(int)], 0, (255, 255, 0), 2)
        self.show_image()

        moments = cv.moments(box)
        x = int(moments["m10"] / moments["m00"]) if moments["m00"] != 0 else 320
        return self.image, x, area
        

    def show_image(self):
        if self.image is not None:
            cv.imshow(self.name, self.image)

        return cv.waitKey(1) & 0xFF == ord("q")

    def get_index(self, ids: MatLike, target_id: int):
        for i in range(len(ids)):
            if int(ids[i]) == target_id:
                return i

        return None

    def __del__(self, *args, **kwargs):
        self.cap.release()
