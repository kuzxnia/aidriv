from time import sleep, time
from picamera import PiCamera
from picamera.array import PiRGBArray
import pygame
from steering import Steering
from pygame.locals import KEYDOWN
import numpy as np
from model import NeuralNetwork
import cv2


class RcDriver(object):
    def __init__(self):
        self.ster = Steering()
        self.camera = PiCamera()
        self.camera.resolution = (320, 240)
        self.rawCapture = PiRGBArray(self.camera, size=(320, 240))
        self.nn = NeuralNetwork()
        self.nn.load_model('nn_model.xml')
        sleep(0.2)

        self.screen = pygame.display.set_mode((320, 240))
        pygame.init()
        print('init complete')

    def collect(self):
        for frameBuf in self.camera.capture_continuous(self.rawCapture, format='rgb', use_video_port=True):
            frame = np.rot90(frameBuf.array)
            self.rawCapture.truncate(0)
            self.screen.fill([0, 0, 0])  # Blank fill the screen
            self.screen.blit(pygame.surfarray.make_surface(frame), (0, 0))  # Load new image on screen

            gray = cv2.cvtColor(frameBuf.array, cv2.COLOR_BGR2GRAY)
            height, width = gray.shape
            roi = gray[int(height / 2):height, :]

            image_array = roi.reshape(1, height, width).astype(np.float32)
            prediction = self.nn.predict(image_array)
            self.handle_prediction(prediction)

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    key_input = pygame.key.get_pressed()
                    if key_input[pygame.K_x] or key_input[pygame.K_q]:
                        print("exit")
                        self.ster.change_motors_speed(0, 0)
                        raise KeyboardInterrupt

            pygame.display.update()  # Update pygame display
        pygame.quit()

    def handle_prediction(self, prediction):
        speed_direction = {
            0: (50, 100, 'Left'),
            1: (50, -100, 'Right'),
            2: (100, 0, 'Up'),
            3: (-100, 0, 'Down'),
            4: (75, 50, 'Up Left'),
            5: (75, -50, 'Up Right')
        }

        forward, turn, message = speed_direction[prediction]

        print(message)
        self.ster.change_motors_speed(forward, turn)
