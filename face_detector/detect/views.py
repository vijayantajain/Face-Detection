"""Module controlling the 'View' of the application"""

import os
from os import path

import numpy as np
from flask import Blueprint, flash, render_template, request
from flask.views import MethodView

from face_detector.detect.detect_faces import get_img_w_faces, save_image
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
    renders the required template
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
        has been filled. First it checks for the validity
        of the inputs through `form.validate` function. If
        the input data in the form is correct then it saves
        the image and calls `get_faces` to get the image file
        containing the detected faces and the number of faces
        detected. It then returns the `render_template` function
        which renders `faces.html` template with the requisite
        context. In case the form input is not valid it 'flashes'
        the respective error and renders the 'form.html' template

        Returns
        -------
        render_template : function
            The function which renders template
        """

        form = InputForm(request.form)

        if form.validate():
            try:
                image = request.files['image']
                if allowed_extension(image.filename):
                    confidence = form.confidence.data
            except KeyError: # TODO - Raise validation error when no image is uploaded
                filename = DEFAULT_IMAGE
            image_w_faces, num_faces = get_img_w_faces(image, confidence)

            #Save the image
            (name, ext) = path.splitext(image.filename)
            image_w_faces_filename = name + '_faces' + ext
            save_image(image_w_faces, UPLOAD_FOLDER, image_w_faces_filename)

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
