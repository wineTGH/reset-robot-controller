import cv2 as cv
from camera import Camera
from trajectories import StartToCenterTrajectory

camera_move = Camera(2, "move")
# camera_platform = Camera(4, "platform")


StartToCenterTrajectory(camera_move).run()
camera_move.release()
cv.destroyAllWindows()