import shlex
import os
import subprocess
import shutil
import time
from datetime import datetime

import cv2
import imutils
from imutils.video import VideoStream


class Camera:
    def __init__(self, path):
        self.vs = VideoStream(usePiCamera=1, resolution=(1280, 960)).start()
        self.frame_full = None
        self.frame = None
        self.resolution = [1280, 960]
        self.path = path
        self.record_video = False
        self.video_path = None

    def get_frames(self):
        time.sleep(2)

        i = 0
        while True:
            self.frame_full = self.vs.read()
            self.frame = imutils.resize(self.frame_full, width=320, height=240)
            if self.record_video:
                i+=1
                self.take_picture(i)
                time.sleep(0.05)
                continue
            else:
                i=0
            time.sleep(0.01)

    def take_picture(self, i=None):
        date_string = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        width, height = self.resolution
        picture = imutils.resize(self.frame_full, width=width, height=height)
        if i is None:
            start = datetime.now()
            cv2.imwrite(f'{self.path}{date_string}.jpg', picture)
        else:
            cv2.imwrite(f'{self.video_path}/{i:05}.jpg', picture)

    def start_video(self):
        date_string = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        self.video_path = f'{self.path}{date_string}'
        os.mkdir(self.video_path)
        self.record_video = True

    def stop_video(self):
        self.record_video = False
        command = f"ffmpeg -ts_from_file 2 -i {self.video_path}'/%5d.jpg' -vsync 1 -r 15 {self.video_path}.mp4"
        p = subprocess.Popen(shlex.split(command), stdin=subprocess.PIPE, text=True)
        p.wait()
        shutil.rmtree(self.video_path)
        self.video_path = None
