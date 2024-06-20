import imutils
import cv2
import os
import time 
import schedule
from ultralytics import YOLO
import cvzone
import pandas as pd

model = YOLO('best.pt')
# result = model.track(source='vdo_test_1.mp4', save=True, project="runs/detect", exist_ok=True)
# result = model.track(source='vdo_test_1.mp4', show=True)
line_position = 950
enter_count = 0
exit_count = 0

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.line(frame, (line_position, 0), (line_position, frame.shape[0]), (0, 255, 0), 2)
    cv2.imshow('People Counting', frame)


cv2.waitKey(1)

