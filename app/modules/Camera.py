# Camera.py

import cv2
import numpy as np

class Camera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        image = cv2.flip(image, 1)
        height, width = np.size(image, 0), np.size(image, 1)
        start = (width - height)/2
        end = start + height
        cv2.rectangle(image, (start, 0), (end, height), (243, 150, 33), 5)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def get_pic(self):
        cap = cv2.VideoCapture(0) # says we capture an image from a webcam
        _,cv2_im = cap.read()
        return cv2.cvtColor(cv2_im,cv2.COLOR_BGR2RGB)
