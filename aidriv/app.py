from gevent import monkey
monkey.patch_all()

import os
from shutil import disk_usage

import cv2
from flask import Flask, Response, render_template, send_file
from flask_sockets import Sockets
from gevent import sleep, spawn
from keras.models import load_model

from camera import Camera
from steering import Steering
from lane_detection import getLaneCurve
from utils import get_prediction, getClassName, localization

GALLERY_ROOT_DIR = os.path.join(os.path.dirname(__file__), 'static', 'gallery', '')

app = Flask(__name__, static_folder='static')
app.config['GALLERY_FOLDER'] = GALLERY_ROOT_DIR
sockets = Sockets(app)
steering = Steering()
camera = Camera(app.config['GALLERY_FOLDER'])
model = load_model('model.h5')
ai_mode = False

#creating greenthread for getting frames from camera
spawn(camera.get_frames)


def generate(cam):
    while True:
        if cam.frame is None:
            sleep(0.01)
            continue
        if ai_mode:
            frame, curve = getLaneCurve(cam.frame, -1)

            coordinate, image, sign = localization(
                cam.frame,
                300,  # min_components_size,
                0.65  # similitary_contour_with_circle
            )

            # for specific size
            if coordinate:  # and 90 > x > 40 and 90 > y > 40:
                x, y, z = sign.shape
                # scale sign to 32x32
                prediction = get_prediction(model, sign)

                frame = cv2.rectangle(frame, coordinate[0], coordinate[1], (255, 255, 255), 1)
                print(prediction)
                if prediction > 0:
                    text = getClassName(prediction)  # fill with correct class
                    cv2.putText(frame, text, (coordinate[0][0], coordinate[0][1] - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2, cv2.LINE_4)

            print(f'curve {curve}')
            if abs(curve) > 25:
                curve *= -2
                if abs(curve) > 100:
                    curve = 100 if curve > 0 else -100
                steering.change_motors_speed_ai(75, curve)
            else:
                steering.change_motors_speed_ai(100, curve * -2)

            # czy konieczne
            #sleep(1/10 - 1/500)
            #steering.change_motors_speed(0, 0)
            #sleep(1/500)
        else:
            frame = cam.frame

        flag, encodedImage = cv2.imencode(".jpg", frame)
        cam.frame = None

        # ensure the frame was successfully encoded
        if not flag:
            continue

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')
        
        sleep(0.01)


@sockets.route('/')
def echo_socket(ws):
    global ai_mode
    while not ws.closed:
        mess = ws.receive()
        message = mess.split()
        if message[0] == 'take_pic': camera.take_picture()
        elif message[0] == 'start_video': camera.start_video()
        elif message[0] == 'stop_video': spawn(camera.stop_video)
        elif message[0] == 'resolution': camera.resolution = tuple(int(n) for n in message[1].split('x'))
        elif message[0] == 'ai_true': 
            ai_mode = True
            print(f'ai mode {ai_mode}')
        elif message[0] == 'ai_false': 
            ai_mode = False
            steering.change_motors_speed(0, 0)
            print(f'ai mode {ai_mode}')
        elif message[0] == 'disk_usage':
            stats = disk_usage("/")
            ws.send(f"{stats.total} {stats.used}")
        elif not ai_mode:
            forward, turn = mess.split()
            steering.change_motors_speed(int(forward), int(turn))
    steering.change_motors_speed(0, 0)


@app.route('/', methods=['GET'])
def index():
    """App home page."""
    return render_template('index.html')


@app.route('/gallery', methods=['GET'])
def gallery():
    """Gallery page"""
    files = [f for f in os.listdir(app.config['GALLERY_FOLDER']) if os.path.isfile(os.path.join(app.config['GALLERY_FOLDER'], f))]
    files = sorted(files, reverse=True)
    return render_template('gallery.html', files=files)


@app.route("/<path:path>")
def static_files(path):
    return send_file(path)


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(generate(camera), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('0.0.0.0', 8000), app, handler_class=WebSocketHandler)
    server.serve_forever()
