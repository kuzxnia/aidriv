from time import sleep
from picamera import PiCamera
from picamera.array import PiRGBArray
from datetime import datetime
from getkey import getkey, keys
import cv2


end = False
screens = 0
while not end:
    direction = ''
    print('waiting for key...')

    key = getkey()
    if key == keys.UP:
        direction = 'U'
    elif key == keys.DOWN:
        direction = 'D'
    elif key == keys.LEFT:
        direction = 'L'
    elif key == keys.RIGHT:
        direction = 'R'
    elif key == 'q':
        end = True
        continue

    camera.capture(rawCapture, format='bgr', resize=(320, 240))
    image = rawCapture.array

    date = datetime.now().strftime("%H_%M_%S")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape
    roi = gray[int(height / 2):height, :]
    cv2.imwrite('screens/%s_%s.jpg' % (direction, date), roi)
    screens += 1
    print('saved')
    rawCapture.truncate(0)

print('saved ' + screens)
