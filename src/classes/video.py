import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread


"""
    changed a bit from:
    https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/
    
"""



class VideoStream():
    def __init__(self, res=(320,240), fps=32, hf=False, vf=False):
        self.camera = PiCamera()
        # set Vertical and Horizontal flip incase camera is mounted in different orientations
        self.camera.vflip = vf
        self.camera.hflip = hf

        # set resolution and fps
        self.camera.resolution = res
        self.camera.framerate = fps

        self.raw_capture = PiRGBArray(self.camera, size=res)
        self.stream = self.camera.capture_continuous(self.raw_capture, format="bgr", use_video_port=True)

        #initialize frame variable
        self.frame = None
        #variable to check if stream should be stopped
        self.stopped = False

        #initialize video thread
        self.video_thread = Thread(target=self.update, args=())

    def start(self):
        # start video thread
        self.video_thread.start()
        return self

    def update(self):
        for frame in self.stream:
            self.frame = frame.array
            self.raw_capture.truncate(0)

            if(self.stopped):
                self.stream.close()
                self.raw_capture.close()
                self.camera.close()
                return

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True


