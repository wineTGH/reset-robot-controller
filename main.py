import cv2 as cv
from camera import Camera
from trajectories import StartToCenterTrajectory

camera = Camera(3)
StartToCenterTrajectory(camera).run()
camera.release()
cv.destroyAllWindows()