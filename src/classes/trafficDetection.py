from enum import Enum

import cv2


class State(Enum):
    STOP = 1
    GO = 2
    SLOW = 3


class TrafficClassifier():

    def __init__(self, classifier_path):
        self.__state = State.GO
        #Load classifier from path provided
        self.classifier = cv2.CascadeClassifier(classifier_path)

    def classify(self, classifier, img):
        #convert BGR image to Grayscale to detect
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        lights = self.classifier.detectMultiScale(gray_img)

        for (x, y, w, h) in lights:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi = gray_img[y + 5:y + h - 5, x + 5:x + w - 5]

            mask = cv2.GaussianBlur(roi, (25, 25), 0)
            min, max, min_loc, max_loc = cv2.minMaxLoc(mask)

            cv2.circle(img, max_loc, 5, (255, 0, 0), 2)

            # TODO: check for green/red lights, set go/stop flags

    def get_state(self):
        return self.__state

