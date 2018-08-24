"""Module for detecting faces"""

import os
from os import path

import numpy as np

import cv2

CWD = os.getcwd()
PROTO_PATH = path.join(CWD, 'face_detector', 'model', 'deploy.prototxt.txt')
MODEL_PATH = path.join(CWD, 'face_detector', 'model', 'res10_300x300_ssd_iter_140000.caffemodel')
IMAGE_PATH = path.join(CWD, 'face_detector', 'static', 'images')

def get_faces(image_name, confidence, image_w_faces='_faces'):
    """Returns the filename of image with bounding boxes around faces
    and the number of faces detected

    Parameters
    ----------
    image_name : str
        The filename of the image
    confidence : float
        The threshold confidence above which to detect faces
    image_w_faces : str, optional
        Phrase which is added to the original image filename 
        and used to save the image after drawing the bounding
        boxes around faces (default : '_faces')

    Returns
    -------
    img_w_faces : str
        Returns the filename by which the image is stored
    num_faces : int
        Number of faces detected in the image with confidence
        greater than the input confidence
    """

    num_faces = 0
    net = cv2.dnn.readNetFromCaffe(PROTO_PATH, MODEL_PATH)
    image = cv2.imread(path.join(IMAGE_PATH, image_name))
    (height, width) = image.shape[:2]

    # PRE-PROCESSING
    # blobFromImage is a pre-processing function that subtracts mean and scales down
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)),
                                 1.0,
                                 (300, 300),
                                 (104.0, 177.0, 123.0),
                                 True)

    # DETECT FACES
    net.setInput(blob)
    detections = net.forward()

    # DRAW FACES
    for i in range(detections.shape[2]):
        conf = detections[0, 0, i, 2] # The probability with detection

        if conf > confidence:
            num_faces += 1
            box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
            (start_x, start_y, end_x, end_y) = box.astype('int')

            text = "{:.2f}%".format(conf * 100)
            text_y = start_y - 10 if start_y - 10 > 10 else start_y + 10
            cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
            cv2.putText(image, text, (start_x, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

    # cv2.imshow('Faces', image)
    # cv2.waitKey(0)
    (name, ext) = path.splitext(image_name)
    image_w_faces = name + '_faces' + ext
    cv2.imwrite(path.join(IMAGE_PATH, image_w_faces), image)
    return image_w_faces, num_faces
