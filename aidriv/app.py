from gevent import monkey
monkey.patch_all()

import os
from shutil import disk_usage
from datetime import datetime, timedelta

import cv2
from flask import Flask, Response, render_template, send_file, request
from flask_sockets import Sockets
from gevent import sleep, spawn
from keras.models import load_model

from camera import Camera
from steering import Steering
from lane_detection import getLaneCurve
from utils import get_prediction, getClassName, localization
from track_bar_vals import initialTrackBarVals

GALLERY_ROOT_DIR = os.path.join(os.path.dirname(__file__), 'static', 'gallery', '')

app = Flask(__name__, static_folder='static')
app.config['GALLERY_FOLDER'] = GALLERY_ROOT_DIR
sockets = Sockets(app)
steering = Steering()
camera = Camera(app.config['GALLERY_FOLDER'])
model = load_model('model.h5')
ai_mode = False
speed = 65
stoped = False
################################
stop_time = datetime.now()
calibration = False
copy_track_vals = initialTrackBarVals.copy()

#creating greenthread for getting frames from camera
spawn(camera.get_frames)


def generate(cam):
    global speed, stoped, calibration, stop_time
    while True:
        prediction = -1
        coordinate = None
        x, y , z = 0, 0, 0
        if cam.frame is None:
            sleep(0.01)
            continue
        if ai_mode or calibration:
            frame, curve = getLaneCurve(cam.frame, initialTrackBarVals, -1)

            coordinate, image, sign = localization(
                cam.frame,
                300,  # min_components_size,
                0.65  # similitary_contour_with_circle
            )

            # for specific size
            if coordinate and not calibration:  # and 90 > x > 40 and 90 > y > 40:
                x, y, z = sign.shape
                # scale sign to 32x32

                prediction = get_prediction(model, sign)[0]

                frame = cv2.rectangle(frame, coordinate[0], coordinate[1], (255, 255, 255), 1)
                text = getClassName(prediction)
                print(text, x, y)
                cv2.putText(frame, text, (coordinate[0][0], coordinate[0][1] - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2, cv2.LINE_4)

            curve *= 2
            if abs(curve) > 100:
                curve = 100 if curve > 0 else -100
            if prediction in [2, 3] and not stoped and stop_time + timedelta(seconds=12) < datetime.now():
                print('ZATRZYMANIE W CURVE')
                steering.change_motors_speed(0,0)
            elif ai_mode and not stoped:
                print(f'curve {curve}')
                steering.change_motors_speed_ai(speed, curve)
        else:
            frame = cam.frame

        flag, encodedImage = cv2.imencode(".jpg", frame)
        cam.frame = None

        # ensure the frame was successfully encoded
        if not flag:
            continue

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')
        
        if ai_mode and coordinate:# and 90 > x > 25 and 90 > y > 25:
            if prediction == 0:
                speed = 60
                print('#####################   WYKRYTO 30')
            elif prediction == 1:
                speed = 65
                print('#####################   WYKRYTO 70')
            elif prediction == 2:
                print('#####################   WYKRYTO stop')
                if not stoped and stop_time + timedelta(seconds=12) < datetime.now():
                    print('ZATRZYMANIE ZE SLEEPEM')
                    steering.change_motors_speed(0, 0)
                    #sleep(4)
                    stoped = True
                    stop_time = datetime.now()
            elif prediction == 3:
                print('#####################   WYKRYTO zakaaz')
                steering.change_motors_speed(0, 0)
                sleep(4)

        if stop_time + timedelta(seconds=4) < datetime.now():
            stoped = False

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


@sockets.route('/calibration')
def echo_socket(ws):
    global initialTrackBarVals
    while not ws.closed:
        mess = ws.receive()
        print(mess)
        vals = []
        for m in mess.split(','):
            vals.append(int(m))
        initialTrackBarVals = vals

@app.route('/', methods=['GET', 'POST'])
def index():
    """App home page."""
    global initialTrackBarVals, calibration, copy_track_vals
    calibration = False
    if request.method == 'POST':
        print('indeex ', request.form)
        vals = []
        for name, val in request.form.items():
            if name == 'zapisz':
                continue
            elif name == 'anuluj':
                initialTrackBarVals = copy_track_vals
                return render_template('index.html')
            vals.append(int(val))
        print('po returnie z anulacji')
        initialTrackBarVals = copy_track_vals = vals
        vals = map(str, vals)
        vals = ' ,'.join(vals) 
        f = open('track_bar_vals.py', 'w')
        f.write('initialTrackBarVals = [' + vals + ']')
        f.close()
    return render_template('index.html')


@app.route('/gallery', methods=['GET'])
def gallery():
    """Gallery page"""
    files = [f for f in os.listdir(app.config['GALLERY_FOLDER']) if os.path.isfile(os.path.join(app.config['GALLERY_FOLDER'], f))]
    files = sorted(files, reverse=True)
    return render_template('gallery.html', files=files)


@app.route('/settings', methods=['GET'])
def settings():
    """Settings page"""
    global calibration
    calibration = True
    print('settings: ', initialTrackBarVals)
    return render_template('settings.html', values=initialTrackBarVals)


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
