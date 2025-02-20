import cv2 as cv
from camera import Camera
from trajectories import StartToCenterTrajectory

camera = Camera(3)
StartToCenterTrajectory(camera).run()
# while True:
#     print(camera.read_marker(2))
camera.release()
cv.destroyAllWindows()