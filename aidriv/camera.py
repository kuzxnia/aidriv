from time import sleep

import imutils
from imutils.video import VideoStream


class Camera:
    def __init__(self):
        self.vs = VideoStream(usePiCamera=1).start()
        self.frame = None

    def get_frames(self):
        sleep(2)

        while True:
            self.frame = self.vs.read()
            #self.frame = imutils.resize(self.frame, width=400)
            #self.frame = imutils.rotate(self.frame, angle=180)
            sleep(0.02)
