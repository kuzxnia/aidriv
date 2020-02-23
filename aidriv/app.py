import os

from bottle import route, run, static_file

path = os.path.abspath(__file__)
static_dir_path = os.path.dirname(os.path.dirname(path)) + "/static/"


@route("/")
def index():
    return static_file("index.html", root=static_dir_path)


@route(r"/<filename:re:.*\.png>")
def images(filename):
    return static_file(filename, root=static_dir_path, mimetype="image/png")


@route("/<filename:path>")
def static_files(filename):
    return static_file(filename, root=static_dir_path)


run(host="localhost", port=8080)
