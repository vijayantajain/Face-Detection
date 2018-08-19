"""Module the 'face_detector' flask app"""

import os
from os import path

from flask import Flask
from face_detector.detect.views import detect_faces

CWD = os.getcwd()
INSTANCE_PATH = path.join(CWD, 'instance')

app = Flask(__name__, instance_path=INSTANCE_PATH, instance_relative_config=True)
app.config.from_pyfile('config.py')
app.register_blueprint(detect_faces)
