from time import sleep, time
from picamera import PiCamera
from picamera.array import PiRGBArray
import pygame
import cv2
from steering import Steering
from pygame.locals import KEYDOWN
import numpy as np
import lane_detection

freq = 50

left_in1, left_in2, left_pwm = 26, 19, 21
right_in3, right_in4, right_pwm = 13, 6, 5


class CollectData(object):
    def __init__(self):
        self.ster = Steering()
        self.camera = PiCamera()
        self.camera.resolution = (320, 240)
        self.rawCapture = PiRGBArray(self.camera, size=(320, 240))
        sleep(0.2)

        self.saved_frame = 0

        self.screen = pygame.display.set_mode((320, 240))
        pygame.init()
        print('init complete')

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def collect(self):
        direction = ''
        for frameBuf in self.camera.capture_continuous(self.rawCapture, format='rgb', use_video_port=True):
            start_calc = time()

            frame, curve = lane_detection.getLaneCurve(frameBuf.array, -1)

            # frame = np.rot90(frameBuf.array)
            self.rawCapture.truncate(0)
            self.screen.fill([0, 0, 0])  # Blank fill the screen
            self.screen.blit(pygame.surfarray.make_surface(frame), (0, 0))  # Load new image on screen

            self.ster.change_motors_speed(50, curve * -1)
            try:
                for event in pygame.event.get():
                    self.handle_key_event(event, direction)
            except KeyboardInterrupt:
                print('ending')
                break

            calc = 1 / 10 - (time() - start_calc)
            if calc > 0:
                sleep(calc)

            pygame.display.update()  # Update pygame display
        print(f'saved frames {self.saved_frame}')
        pygame.quit()

    def handle_key_event(self, event):
        if event.type == KEYDOWN:
            key_input = pygame.key.get_pressed()

            if key_input[pygame.K_x] or key_input[pygame.K_q]:
                print("exit")
                self.ster.change_motors_speed(0, 0)
                raise KeyboardInterrupt

        elif event.type == pygame.KEYUP:
            print('stop')
            self.ster.change_motors_speed(0, 0)


if __name__ == '__main__':
    c = CollectData()
    c.collect()
