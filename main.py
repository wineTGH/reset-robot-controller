from camera import Camera
from trajectories import StartToCenterTrajectory, BoxesTrajectory, FirstBoxesToFinish

camera_move = Camera(17, "move")
camera_platform = Camera(15, "platform")
StartToCenterTrajectory(camera_move).run()
BoxesTrajectory(camera_platform).run()
FirstBoxesToFinish(camera_move).run()

# while True:
    # print(camera_move.read_marker(2))
    # print(camera_platform.read_marker(1))