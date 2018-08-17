"""Module controlling the 'View' of the application"""

from os import path

from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename

detect_faces = Blueprint(__name__, 'detect_faces')

@detect_faces.route('/', methods=['GET', 'POST'])
def process_form():
    """This function extracts the image
    and the confidence from the request
    and returns the image with faces drawn
    """

    #TODO - Instantiate Form
    if request.method == 'GET':
        return render_template('form.html')

    if request.method == 'POST':
        return render_template('faces.html')



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
    # if path.splitext(filename)[-1] in app.config['ALLOWED_EXTENSIONS']:
    #     val = True

    return val
