"""Module controlling the 'View' of the application"""

import os
from os import path

from flask import Blueprint, flash, render_template, request
from flask.views import MethodView

from face_detector.detect.detect_faces import FaceDetector
from face_detector.detect.forms import InputForm, allowed_extension

CWD = os.getcwd()
UPLOAD_FOLDER = path.join(CWD, 'face_detector', 'static', 'images')
DEFAULT_IMAGE = 'obama.png'

detect_faces = Blueprint(__name__, 'detect_faces')

class FormView(MethodView):
    """Class handling the view of the form.

    There are two methods `get` and `set` which
    handle the respective request and accordingly
    returns the `render_template` function which
    renders the respective template
    """

    def get(self):
        """This method handles the GET request from the user
        which is when the main page is loaded.

        This method returns the form.html page with context as
        Input form

        Returns
        -------
        render_template : function
            The function which renders the form.html
        """
        form = InputForm(request.form)
        return render_template('form.html', form=form)

    def post(self):
        """Handles the POST request from the user

        This method handles the request after the form
        has been filled. It checks for the validity of the
        input form. In case of an erronous input it renders
        the same template with errors. In case there are no
        input errors it then initializes `FaceDetector` to
        detect faces and then renders that image to the user

        Returns
        -------
        render_template : function
            The function which renders template
        """

        form = InputForm(request.form)

        if form.validate():

            image = request.files['image']
            if not allowed_extension(image.filename):
                return render_template('form.html', form=form)

            confidence = form.confidence.data

            # Get faces
            detector = FaceDetector(image)
            image_w_faces, num_faces = detector.get_img_w_faces(confidence=confidence)

            # Save the image
            (name, ext) = path.splitext(image.filename)
            image_w_faces_filename = name + '_faces' + ext
            detector.save_image(image_w_faces, UPLOAD_FOLDER, image_w_faces_filename)

            return render_template(
                'faces.html', filename=image_w_faces_filename, num_faces=num_faces)

        self.flash_errors(form)
        return render_template('form.html', form=form)

    @staticmethod
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

detect_faces.add_url_rule(rule='/', view_func=FormView.as_view('home'))
