import cv2 as cv
from camera import Camera
from trajectories import StartToCenterTrajectory

camera = Camera(2)
StartToCenterTrajectory(camera).run()

camera.release()
cv.destroyAllWindows()