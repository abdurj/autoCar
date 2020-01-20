import cv2
from .classes.vision import *
from .classes.raspberry_pi_control import *
from .classes.video import VideoStream
from . import Constants

stop_threshold = 0


def main():
    # traffic_handler = TrafficClassifier(Constants.PATH_TO_CLASSIFIER)
    face_detector = FaceClassifier(Constants.PATH_TO_CLASSIFIER)
    sensor_handler = SensorData()
    car_controller = CarController()
    video_stream = VideoStream()
    distance_calculator = DistanceCalculator()

    # Allow all sensors/Cameras to warmup
    time.sleep(2)

    while True:
        frame = video_stream.read()
        v = face_detector.detectFace(frame)

        dist = sensor_handler.distance()

        if dist < stop_threshold:
            car_controller.set_output(0, 0)

        else:
            d = distance_calculator.calculate(v, Constants.CAMERA_HEIGHT_OFFSET)

        left_speed = Constants.kP * d
        right_speed = Constants.kP * d

        car_controller.set_output(left_speed, right_speed)


if __name__ == "__main__":
    main()
