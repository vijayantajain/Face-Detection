"""Module for defining the form as well check-functions for form-input"""

from os import path

from flask_wtf import FlaskForm
from wtforms import FileField, FloatField, validators, ValidationError

ALLOWED_EXTENSIONS = ['.jpeg', '.jpg', '.png']

def is_image_uploaded(form, field):
    """Validtor function that ensures that an image
    is uploaded

    Parameters
    ----------
    form : InputForm
        The form object passed
    field : FileField
        The file field in the InputForm class

    Raises
    ------
    ValidationError
        If the image is not uploaded
    """


    if field.data == '':
        raise ValidationError('Image must be uploaded')

class InputForm(FlaskForm):
    """A WTForm used by Jinja to generate HTML

    Parameters
    ----------
    FlaskForm : Class FlaskForm
        InputForm inherits `FlaskForm`
    """

    confidence = FloatField(
        'Confidence', [validators.DataRequired('Confidence is required and must be a float'),
                       validators.NumberRange(min=0.0, max=0.999)])
    image = FileField('Upload an Image', [is_image_uploaded])

def allowed_extension(filename):
    """Checks the file name of the uploaded image

    This function checks if the uploaded image is either jpeg or png.
    Other image formats are not supported

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
    if path.splitext(filename)[-1].lower() in ALLOWED_EXTENSIONS:
        val = True

    return val
