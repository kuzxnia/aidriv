from gevent import monkey
monkey.patch_all()

from flask import Flask, request, render_template, Response, stream_with_context, jsonify, send_file
from gevent import pywsgi
import gevent
import cv2

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__, static_folder='static')


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
    app.run()
    #server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    #server.serve_forever()


