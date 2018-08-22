"""Module to define the form"""

from flask_wtf import FlaskForm
from wtforms import FileField, FloatField, validators

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
    image = FileField('Upload an Image')
