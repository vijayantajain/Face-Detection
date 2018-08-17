"""Module the 'face_detector' flask app"""

from flask import Flask
from face_detector.detect.views import detect_faces

app = Flask(__name__)
app.register_blueprint(detect_faces)
