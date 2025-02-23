from camera import Camera
from trajectories import StartToCenterTrajectory, BoxesTrajectory, FirstBoxesToFinish

camera_move = Camera(2, "move")
camera_qr = Camera(6, "qr")
camera_grab = Camera(4, "platform")
# StartToCenterTrajectory(camera_move).run()

BoxesTrajectory(camera=camera_move, camera_qr=camera_qr, camera_grab=camera_grab).run()
# FirstBoxesToFinish(camera_move).run()

# while True:
    # print(camera_move.read_qr())
    # print(camera_qr.read_qr())
    # print(camera_grab.read_qr())