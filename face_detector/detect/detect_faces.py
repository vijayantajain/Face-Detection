"""Module that defines the FaceDetector class and also image-handling functions"""

import os
from os import path

import numpy as np
from PIL import Image

import cv2

CWD = os.getcwd()
PROTO_PATH = path.join(CWD, 'face_detector', 'model', 'deploy.prototxt.txt')
MODEL_PATH = path.join(CWD, 'face_detector', 'model', 'res10_300x300_ssd_iter_140000.caffemodel')
IMAGE_PATH = path.join(CWD, 'face_detector', 'static', 'images')

class FaceDetector():
    """Class that detects the faces

    Parameters
    ----------
    image : np.ndarray or FileObject
        The image parameter could either be
        a numpy array or a FileObject. Depending
        on the type the image is opened accordingly
    file_object : bool
        Parameter to inform if the `image` attribute
        is passed as a FileObject or not
    prototxt_path : str, optional
        Filepath to the directory where prototxt file is
        stored (default=PROTO_PATH)
    model_path : str, optional
        Filepath to the directory where the Caffe model is
        saved (default=MODEL_PATH)

    Attributes
    ----------
    image, file_object : See Parameters
    height : float
        Height of the image
    width : float
        Width of the image
    net : Caffe Model
        The Caffe pre-trained model
    """

    def __init__(self, image, file_object=True, prototxt_path=PROTO_PATH, model_path=MODEL_PATH):
        if file_object:
            image = np.asarray(Image.open(image))
        self.image = image
        self.height = image.shape[0]
        self.width = image.shape[1]
        self.net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

    def convert_color(self, code):
        """Converts the color of the image

        Usually used to convert from RGB to BGR mode
        for OpenCV

        Parameters
        ----------
        code : OpenCV Code
            The code defining how to convert the color
            of the image

        Returns
        -------
        np.ndarray
            Returns the image with converted color
        """

        return cv2.cvtColor(self.image, code)

    def get_detections(self):
        """Returns the detections as array

        `detections` is a 4D array with the following dimensions -
        [img, channels, num_detections, property]

        The last dimension is `detections` contains following items -
        [UNK, UNK, CONFIDENCE, START_X, START_Y, END_X, END_Y, UNK]
        (UNK is unknown). As there is only 1 image and 1 channel, the
        method only returns the last two dimensions of the array

        Returns
        -------
        detections : np.ndarray
            A 2D array with first dimension being the number of detections
            whereas second being the property dimension
        """

        bgr_image = self.convert_color(cv2.COLOR_RGB2BGR)

        blob = cv2.dnn.blobFromImage(cv2.resize(bgr_image, (300, 300)),
                                     1.0,
                                     (300, 300),
                                     (104.0, 177.0, 123.0),
                                     True)

        self.net.setInput(blob)

        detections = self.net.forward()

        return detections[0, 0, :, :]

    def get_img_w_faces(self, confidence, color=(0, 255, 0)):
        """This method returns the image with bounding boxes drawn
        around face(s) detected and the number of face(s) detected

        Parameters
        ----------
        confidence : flaot
            The threshold confidence below which the detections
            are discarded
        color : tuple, optional
            BGR format color; by default it is green(default=(0, 255, 0))

        Returns
        -------
        image : np.ndarray
            The image with bounding boxes drawn around faces
        num_faces : int
            Number of faces detected
        """
        num_faces = 0

        detections = self.get_detections()

        for i in range(detections.shape[0]):
            probability = detections[i, 2]

            if probability >= confidence:
                num_faces += 1
                text = "{:.2f}%".format(probability * 100)

                (start_x, start_y, end_x, end_y) = self.get_coordinates(detections[i, 3:7])
                text_y = start_y - 10 if start_y - 10 > 10 else start_y + 10

                self.draw_rect((start_x, start_y, end_x, end_y), color)
                self.draw_text(text, (start_x, text_y), color)

        return self.image, num_faces

    def draw_rect(self, box_coordinates, color):
        """Helper method to draw rectangles on image

        It does not returns the image

        Parameters
        ----------
        box_coordinates : tuple
            The coordinates of the box
        color : tuple
            The color with which to draw the rectangle
        """

        cv2.rectangle(self.image, box_coordinates[:2], box_coordinates[2:], color, 2)

    def draw_text(self, text, text_coordinates, color):
        """Helper method to write text on image

        Parameters
        ----------
        text : str
            The text to write on the image
        text_coordinates : tuple
            The start and the end coordinates
        color : tuple
            BGR format color
        """

        cv2.putText(self.image, text, text_coordinates,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)

    def get_coordinates(self, scaled_coordinates):
        """Helper method that returns the dimensions of
        bounding box squares

        The Caffe model returns the coordinates of detections
        between the scale of 0 and 1. Therefore to draw the
        rectangles on the image we need to scale them according
        to the dimensions of the image; which is what this method
        does

        Parameters
        ----------
        scaled_coordinates : tuple
            The dimensions of the boxes between scale between 0 and 1

        Returns
        -------
        tuple
            Box coordinates scaled according to image as int
        """

        box_coordinates = scaled_coordinates * np.array(
            [self.width, self.height, self.width, self.height])

        return box_coordinates.astype('int')

    @staticmethod
    def save_image(image, dir_path, filename):
        """Helper method to save the image

        Parameters
        ----------
        image : np.ndarray
            The image to be saved
        dir_path : str
            The filepath of the directory where the
            image needs to be saved
        filename : str
            Name of the file by which the method
            will in `dir_path`
        """
        try:
            assert path.isdir(dir_path)
        except AssertionError:
            os.mkdir(dir_path)
        img = Image.fromarray(image)
        img.save(path.join(dir_path, filename))
