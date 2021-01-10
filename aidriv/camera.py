import shlex
import os
import subprocess
import time
from datetime import datetime

import cv2
import imutils
from imutils.video import VideoStream


class Camera:
    def __init__(self, path):
        self.vs = VideoStream(usePiCamera=1, resolution=(1280, 960), framerate=25).start()
        self.frame_full = None
        self.frame = None
        self.resolution = (1280, 960)
        self.path = path
        self.start_record = False
        self.stop_record = False

    def get_frames(self):
        print('starting camera')
        time.sleep(2)
        print('camera started')

        while True:
            self.frame_full = self.vs.read()

            self.frame = imutils.resize(self.frame_full, width=320, height=240)
            if self.start_record:
                date_string = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
                self.vs.camera.start_recording(f'{self.path}{date_string}.h264', resize=self.resolution)
                self.start_record = False
            if self.stop_record:
                self.vs.camera.stop_recording()
                self.stop_record = False
            time.sleep(0.01)

    def take_picture(self, i=None):
        date_string = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        width, height = self.resolution
        picture = imutils.resize(self.frame_full, width=width, height=height)
        cv2.imwrite(f'{self.path}{date_string}.jpg', picture)

    def start_video(self):
        self.start_record = True

    def stop_video(self):
        self.stop_record = True
        date_string = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        for file in os.listdir(self.path):
            if file.endswith(".h264"):
                convert = f"MP4Box -add {self.path}{file} {self.path}{date_string}.mp4"
                p = subprocess.Popen(shlex.split(convert), stdin=subprocess.PIPE, text=True)
                p.wait()
                os.remove(f'{self.path}{file}')
