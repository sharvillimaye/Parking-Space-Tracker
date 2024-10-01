import cv2 as cv
import pickle
import cvzone
import numpy as np

video = cv.VideoCapture('carPark.mp4')
width, height = 107, 48
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

def checkparking(processed):
    spaces = 0
    for pos in posList:
        x, y = pos
        cropped = processed[y:y+height, x:x+width]
        count = cv.countNonZero(cropped)
        cvzone.putTextRect(frame, str(count), (x, y+height-10), scale=1.5, thickness=2, offset=0)

        if count < 800:
            color = (0, 255, 0)
            thickness = 5
            spaces += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv.rectangle(frame, pos, (pos[0] + width, pos[1] + height), color, thickness)

    cvzone.putTextRect(frame, f'Free: {spaces}/{len(posList)}', (50, 60), thickness=3, offset=20,
                       colorR=(0, 200, 0))

while True:
    ret, frame = video.read()
    if not ret:
        video.set(cv.CAP_PROP_POS_FRAMES, 0)
        ret, frame = video.read()
    frame_grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_blur = cv.GaussianBlur(frame_grey, (3, 3), 1)
    frame_thresh = cv.adaptiveThreshold(frame_blur,255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 16)
    frame_median = cv.medianBlur(frame_thresh, 5)
    kernel = np.ones((3, 3), np.uint8)
    frame_dilated = cv.dilate(frame_median, kernel, iterations=1)

    checkparking(frame_dilated)



    cv.imshow('Parking Tracker', frame)
    if cv.waitKey(10) & 0xFF == ord('q'):
        break