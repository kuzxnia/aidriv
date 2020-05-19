from gevent import monkey
monkey.patch_all()

from flask import Flask, request, render_template, Response, stream_with_context, jsonify, send_file, url_for
from gevent import pywsgi
from flask_sockets import Sockets
from geventwebsocket.handler import WebSocketHandler
#import gevent
from time import sleep
import cv2

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__, static_folder='static')
sockets = Sockets(app)


@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        print(message)
        ws.send(message)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


@app.route("/<path:path>")
def static_files(path):
    return send_file(path)


@stream_with_context
def gen():
    """Video streaming generator function."""
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise RuntimeError('Could not start camera.')

    while True:
        sleep(0)
        # read current frame
        _, img = camera.read()

        # encode as a jpeg image and return it
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 8000), app, handler_class=WebSocketHandler)
    server.serve_forever()


