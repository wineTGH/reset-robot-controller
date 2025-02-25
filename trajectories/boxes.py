from arduino import arduino, servo
import time
import state
from trajectories.base import Trajectory

class BoxesTrajectory(Trajectory):
    def __init__(self, camera, camera_qr, camera_grab):
        if not camera_grab or not camera_qr:
            raise FileNotFoundError("не найдены камеры захвата и qr")
        
        super().__init__(camera, camera_qr, camera_grab)

    def run(self) -> bool:
        arduino.write("PG:140;")
        time.sleep(1)
        return self.drive_to_qr_code()

    def drive_to_qr_code(self):
        count = 0

        while True:
            _, data, _, _ = self.camera_qr.read_qr()

            # если мы не увидели QR код, то продолжаем двигаться
            if data is None:
                arduino.write("MF:20;")
                continue
            
            count += 1
            arduino.write("MS:0;")
            is_loaded = self.handle_box()
            if is_loaded:
                return True
            
            # если проехали три ящика и ничего не нашли, разворачиваемся
            if count == 3:
                arduino.write("MY:-180;")
                time.sleep(2)
            else:
                # Отъезжаем от QR кода, чтобы камера его снова не прочитала
                arduino.write("MF:20;")
                time.sleep(2)

            if count == 6:
                return False
        
        
    def grab_lower_part(self):
        arduino.write("PG:140;")
        servo.write("GO;")
        time.sleep(2)
        servo.write("PF;")
        time.sleep(3)
        servo.write("GC;")
    
    def grab_higher_part(self):
        arduino.write("PP:1;")
        time.sleep(16)
        arduino.write("PG:430;")
        time.sleep(4)
        servo.write("GO;")
        time.sleep(2)
        servo.write("PF;")
        time.sleep(5)
        servo.write("GC;")
        arduino.write("PA:1;")
        time.sleep(10)
        servo.write("PB;")
        arduino.write("PA:0;")

    def handle_box(self):
        _, data, _, _ = self.camera_qr.read_qr()
        # Если товар с нижнего QR-кода есть в списке заказных товаров, то берём его
        if data.lower() in state.order_items:
            self.grab_lower_part()

            # вычеркиваем товар из списка
            state.order_items.remove(data.lower())
            return True
        
        #* эта часть кода выполнится, только если на первой полке ничего нет *#

        # Поднимаем шаговик, чтобы посмотреть код сверху
        #TODO: протестируете это кол-во шагов. Видит ли он код или нет
        arduino.write("PG:500;")
        time.sleep(2)
        _, data, _, _ = self.camera_grab.read_qr()

        # Если товар с нижнего QR-кода есть в списке заказных товаров, то берём его
        if data.lower() in state.order_items:
            self.grab_higher_part()

            # вычеркиваем товар из списка
            state.order_items.remove(data.lower())
            return True
        
        #* этот код выполнится только если и на первой и на второй полке нет ничего нам нужного *#

        # Убираем шаговик в предыдущие состояние
        arduino.write("PG:140;")
        time.sleep(1)

        # Говорим, что ничего не собрали
        return False