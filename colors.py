import cv2 as cv

cap = cv.VideoCapture(0)

def none(x):
    pass

controlsWin = "Frame"
cv.namedWindow(controlsWin)
cv.createTrackbar("L_l", controlsWin, 0, 255, none)
cv.createTrackbar("A_l", controlsWin, 130, 255, none)
cv.createTrackbar("B_l", controlsWin, 0, 255, none)

cv.createTrackbar("L_u", controlsWin, 130, 255, none)
cv.createTrackbar("A_u", controlsWin, 186, 255, none)
cv.createTrackbar("B_u", controlsWin, 126, 255, none)

while True:
    cv.waitKey(1)
    ret, image = cap.read()

    g_frame = cv.cvtColor(image, cv.COLOR_BGR2LAB)
    g_frame = cv.GaussianBlur(g_frame, (9, 9), 3)
    g_frame = cv.inRange(
        g_frame,
        (
            cv.getTrackbarPos("L_l", controlsWin),
            cv.getTrackbarPos("A_l", controlsWin),
            cv.getTrackbarPos("B_l", controlsWin),
        ),
        (
            cv.getTrackbarPos("L_u", controlsWin),
            cv.getTrackbarPos("A_u", controlsWin),
            cv.getTrackbarPos("B_u", controlsWin),
        ),
    )

    if g_frame is None:
        cv.imshow("Frame", image)
        cv.imshow("Mask", g_frame)
        continue

    cnt, h = cv.findContours(g_frame, 1, cv.CHAIN_APPROX_SIMPLE)
    
    if len(cnt) == 0:
        cv.imshow("Frame", image)
        cv.imshow("Mask", g_frame)
        continue

    cnt = max(cnt, key=cv.contourArea)
    # epsilon = cv.arcLength(cnt, True) * (cv.getTrackbarPos("%", controlsWin) / 100)
    # approx = cv.approxPolyDP(cnt, epsilon, True)

    approx = cv.convexHull(cnt)
    rect = cv.minAreaRect(approx)
    box = cv.boxPoints(rect)

    cv.drawContours(image, [box.astype(int)], 0, (0, 0, 255), 2)
    cv.drawContours(image, [approx.astype(int)], 0, (255, 255, 0), 2)


    cv.imshow("Frame", image)
    cv.imshow("Mask", g_frame)