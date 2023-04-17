#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask server to stream video from a camera.
"""

from flask import Flask, Response
from flask_cors import CORS

from stream_source import StreamSource

app = Flask(__name__.split(".")[0])
CORS(app, origins="*")

camera_to_stream = 0
try:
    camera = StreamSource(camera_to_stream)
except ValueError as err:
    print(err)
    exit(1)


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/stream", methods=["POST"])
def stream():
    image_data = camera.get_frame()

    response = Response(image_data, mimetype="image/jpeg")
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


if __name__ == "__main__":
    app.run()
