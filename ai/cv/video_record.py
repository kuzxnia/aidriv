from time import sleep, time
from picamera import PiCamera
from picamera.array import PiRGBArray
import pygame
import cv2
from steering import Steering
from pygame.locals import KEYDOWN
import numpy as np

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

        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        self.out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (320, 240))

        self.screen = pygame.display.set_mode((320, 240))
        pygame.init()
        print('init complete')

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.out.release()
        cv2.destroyAllWindows()

    def collect(self):
        direction = ''
        for frameBuf in self.camera.capture_continuous(self.rawCapture, format='rgb', use_video_port=True):

            start_calc = time()
            frame = np.rot90(frameBuf.array)
            self.rawCapture.truncate(0)
            self.screen.fill([0, 0, 0])  # Blank fill the screen
            self.screen.blit(pygame.surfarray.make_surface(frame), (0, 0))  # Load new image on screen

            try:
                for event in pygame.event.get():
                    direction = self.handle_key_event(event, direction)
            except KeyboardInterrupt:
                print('ending')
                break

            calc = 1 / 10 - (time() - start_calc)
            if calc > 0:
                sleep(calc)

            self.out.write(frameBuf.array)  # frameBuf.array

            pygame.display.update()  # Update pygame display
        print(f'saved frames {self.saved_frame}')
        pygame.quit()

    def handle_key_event(self, event, direction):
        direction = direction
        if event.type == KEYDOWN:
            key_input = pygame.key.get_pressed()

            if key_input[pygame.K_UP]:
                print("Forward")
                self.ster.change_motors_speed(100, 0)
                direction = 'U'

            elif key_input[pygame.K_DOWN]:
                self.ster.change_motors_speed(-100, 0)
                print("Reverse")

            elif key_input[pygame.K_RIGHT]:
                direction = 'R'
                self.ster.change_motors_speed(25, -100)
                print("Right")

            elif key_input[pygame.K_LEFT]:
                direction = 'L'
                self.ster.change_motors_speed(25, 100)
                print("Left")

            elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                print("exit")
                self.ster.change_motors_speed(0, 0)
                raise KeyboardInterrupt

        elif event.type == pygame.KEYUP:
            print('stop')
            self.ster.change_motors_speed(0, 0)

        return direction


if __name__ == '__main__':
    c = CollectData()
    c.collect()
