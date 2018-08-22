"""Module controlling the 'View' of the application"""

import os
from os import path

from flask import Blueprint, flash, render_template, request
from werkzeug.utils import secure_filename

from face_detector.detect.forms import InputForm
from face_detector.detect.detect_faces import get_faces

CWD = os.getcwd()
UPLOAD_FOLDER = path.join(CWD, 'face_detector', 'static', 'images')
DEFAULT_IMAGE = 'obama.png'
ALLOWED_EXTENSIONS = ['.jpeg', '.jpg', '.png']

detect_faces = Blueprint(__name__, 'detect_faces')

@detect_faces.route('/', methods=['GET', 'POST'])
def process_form():
    """This function extracts the image and the confidence
    from the http-request and returns the image with
    bounding boxes around faces.
    """
    form = InputForm(request.form)
    if request.method == 'GET':
        return render_template('form.html', form=form)

    if request.method == 'POST' and form.validate():
        try:
            image = request.files['image']
            if image and allowed_extension(image.filename):
                filename = secure_filename(image.filename)
                image.save(path.join(UPLOAD_FOLDER, filename))
        except KeyError:
            filename = DEFAULT_IMAGE

        confidence = form.confidence.data
        image_w_faces = get_faces(filename, confidence)
        return render_template('faces.html', filename=image_w_faces)

    flash_errors(form)
    return render_template('form.html', form=form)

def flash_errors(form):
    """Function for flashing errors for an invalid input in the form

    Parameters
    ----------
    form : ProfileForm
        Form object containing fields and errors

    """
    for fields, errors in form.errors.items():
        for error in errors:
            flash('Error in the field {} - {}'.format(getattr(form, fields).label.text, error))

def allowed_extension(filename):
    """Checks the file name of the uploaded image

    Parameters
    ----------
    filename : str
        Name of the file

    Raises
    ------
    ValidationError
        When the file name is not `ALLOWED_EXTENSIONS`

    Returns
    -------
    val : bool
        If the filename extension is allowed or not
    """

    val = False
    if path.splitext(filename)[-1] in ALLOWED_EXTENSIONS:
        val = True

    return val
