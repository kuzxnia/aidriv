from gevent import monkey
monkey.patch_all()

import os

import cv2
from flask import (Flask, Response, render_template, send_file,
                   stream_with_context, request)
from flask_sockets import Sockets
from camera import Camera
from steering import Steering
from gevent import spawn, sleep
from shutil import disk_usage

GALLERY_ROOT_DIR = os.path.join(os.path.dirname(__file__), 'static', 'gallery', '')

app = Flask(__name__, static_folder='static')
app.config['GALLERY_FOLDER'] = GALLERY_ROOT_DIR
sockets = Sockets(app)
steering = Steering()
camera = Camera(app.config['GALLERY_FOLDER'])

#creating greenthread for getting frames from camera
spawn(camera.get_frames)

def generate(cam):
    while True:
        if cam.frame is None:
            sleep(0.01)
            continue

        (flag, encodedImage) = cv2.imencode(".jpg", cam.frame)
        cam.frame = None

        # ensure the frame was successfully encoded
        if not flag:
            continue

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')
        
        sleep(0.01)


@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        stats = disk_usage("/")
        ws.send(f"{stats.total} {stats.used}")
        message = ws.receive()
        if message[:6] == 'camera':
            options = message.split()
            if options[1] == 'take_pic':
                camera.take_picture()
            elif options[1] == 'resolution':
                camera.resolution = [int(n) for n in options[2].split('x')]
            elif options[1] == 'start_video':
                camera.start_video()
            elif options[1] == 'stop_video':
                spawn(camera.stop_video)
        else:
            forward, turn = message.split()
            steering.change_motors_speed(int(forward), int(turn))
    steering.change_motors_speed(0, 0)


@app.route('/', methods=['GET'])
def index():
    """Video streaming home page."""
    return render_template('index.html')


@app.route('/gallery', methods=['GET'])
def gallery():
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