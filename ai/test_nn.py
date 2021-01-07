import numpy as np
import cv2
import time
import os
import pygame
from pygame.locals import KEYDOWN
from model import NeuralNetwork


def concat_path(*paths):
    return os.path.join(*paths)


base_path = concat_path(os.path.expanduser('~'), 'screens/')


class TestNN(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((320, 120))
        pygame.init()
        self.nn = NeuralNetwork()
        self.nn.load_model('nn_model.xml')
        print('init complete')

    def test(self):
        amount = 0
        for filename in os.listdir(base_path):
            path = concat_path(base_path, filename)
            if not os.path.isfile(path):
                continue

            print('reading image' + path)
            image = cv2.imread(path, 0)

            frame = np.rot90(image)
            self.screen.fill([0, 0, 0])  # Blank fill the screen
            self.screen.blit(pygame.surfarray.make_surface(frame), (0, 0))  # Load new image on screen

            # reshape the roi image into a vector
            image_array = image.reshape(1, 120 * 320).astype(np.float32)

            prediction = self.nn.predict(image_array)
            amount += self.handle_prediction(prediction)

            try:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        key_input = pygame.key.get_pressed()
                        if key_input[pygame.K_x] or key_input[pygame.K_q]:
                            print("exit")
                            raise KeyboardInterrupt
            except:
                break
            pygame.display.update()  # Update pygame display

        pygame.quit()

    def handle_prediction(self, prediction):
        speed_direction = {
            0: (50, 100, 'Left'),
            1: (50, -100, 'Right'),
            2: (100, 0, 'Up'),
            3: (-100, 0, 'Down'),
        }

        forward, turn, message = speed_direction[prediction[0]]
        if message != 'Up':
            print(message)
            # time.sleep(2)
            return 1
        return 0


if __name__ == '__main__':
    t = TestNN()
    t.test()
