from enum import Enum

import cv2
import numpy as np
import math

cam_matrix = np.array(
    [[610.50109418, 0, 299.49586007],
     [0, 612.69302602, 234.84060349],
     [0, 0, 1]]
)
dist_matrix = np.array(
    [[1.31142627e-01, 5.16696044e-01, -3.34790431e-03, -9.93205013e-03, -3.37928027e+00]]
)
ay = 612.69
v0 = 234.84


class DistanceCalculator():
    def __init__(self):
        self.ay = 612.69
        self.v0 = 234.84
        self.alpha = math.radians(8)

    def calculate(self, v, h):
        d = h / math.tan(self.alpha + math.atan((v - self.v0) / self.ay))
        return d


class FaceClassifier():
    def __init(self, classifier_path):
        self.classifier = cv2.CascadeClassifier(classifier_path)

    def detectFace(self, img):
        v = 0
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = self.classifier.detectMultiScale(gray_img)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            v = y + h

            return v

class TrafficClassifier():

    def __init__(self, classifier_path):
        self.__state = State.GO
        # Load classifier from path provided
        self.classifier = cv2.CascadeClassifier(classifier_path)

    def classify(self, img):
        v = 0
        brightness_threshold = 200

        # convert BGR image to Grayscale to detect
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        lights = self.classifier.detectMultiScale(gray_img)

        for (x, y, w, h) in lights:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            light = gray_img[y + 5:y + h - 5, x + 5:x + w - 5]

            mask = cv2.GaussianBlur(light, (25, 25), 0)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(mask)

            # a light is turned on if difference between max pixel and min pixel is above a certain threshold
            # (determined empirically)

            if max_val - min_val > brightness_threshold:
                # draw a circle around the brightest point
                # (add x and y to coordinates because they are from ROI not image)
                cv2.circle(img, (max_loc[0] + x, max_loc[1] + y), 5, (255, 255, 255), 2)

                # check where the brightest pixel is to see if it is at the top (red) middle (yellow) or bottom (green)

                # Red will be in the top 1/3rd of the light
                upper_red_bound = 0 / 3  # 0
                lower_red_bound = 1 / 3

                # yellow will be in the middle 1/3rd of the light
                upper_yellow_bound = 1 / 3
                lower_yellow_bound = 2 / 3

                # green will be in the bottom 1/3rd of th light
                upper_green_bound = 2 / 3
                lower_green_bound = 3 / 3  # 1

                # compare y val of max pixel to locations
                if upper_red_bound * h < max_loc[1] < lower_red_bound * h:
                    self.__state = State.STOP

                elif upper_yellow_bound * h < max_loc[1] < upper_yellow_bound * h:
                    self.__state = State.SLOW

                elif upper_green_bound * h < max_loc[1] < lower_green_bound * h:
                    self.__state = State.GO

        return v

    def get_state(self):
        return self.__state

