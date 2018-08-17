"""Module for detecting faces"""

import argparse
import imghdr
import os
from os import path

import numpy as np

import cv2

CWD = os.getcwd()

def create_parser():
    """Argument Parser"""
    parser = argparse.ArgumentParser(description=
                                     "CMD line arguments for the image")

    parser.add_argument('--image', type=str,
                        dest='image',
                        help='Path file to the image',
                        required=True)

    parser.add_argument('--proto', type=str,
                        dest='proto',
                        help='Path to Caffe \'deploy\' protoxt file',
                        required=True)

    parser.add_argument('--model', type=str,
                        dest='model',
                        help='Path  to Caffe pre-trained model',
                        required='True')

    parser.add_argument('--confidence', type=float,
                        dest='confidence',
                        help='Confidence threshold for detecting faces',
                        required=True)

    return parser

def check_arguments(arguments):
    """Checks the validity of the commandline arguments
    passed to the function

    Parameters
    ----------
    arguments : dict
        Dictionary of arguments parsed

    Returns
    -------
    arguments : See Parameters

    Raises
    ------
    AssertionError
        In case the file path is not a file
    AssertionError
        In case the image file is neither png/jpeg
    ArithmeticError
        In case the argument confidence is less than 0.0
    """
    if not path.exists(arguments['image']):
        raise FileNotFoundError('Path to the image is invalid')

    if not path.isfile(arguments['image']):
        raise AssertionError('Path for the image is not a even a file')

    if imghdr.what(arguments['image']) not in ['png', 'jpeg']:
        raise AssertionError('Image is neither png or jpeg')

    if not path.exists(arguments['proto']):
        raise FileNotFoundError('Path to the proto file is invalid')

    if not path.isfile(arguments['proto']):
        raise AssertionError('Path to the proto file is not even a file')

    if not path.exists(arguments['model']):
        raise FileNotFoundError('Path to the model file is invalid')

    if not path.isfile(arguments['model']):
        raise AssertionError('Path to the model file is not even a file')

    if arguments['confidence'] < 0:
        raise ArithmeticError('Confidence level should be greater than or equal to 0.00%')

    return arguments


def main():
    "MAIN"
    parser = create_parser()
    arguments = vars(parser.parse_args())

    print("Checking agument validity...")
    check_arguments(arguments)
    print("Aruments are valid!")

    print("[INFO] Loading model...")

    net = cv2.dnn.readNetFromCaffe(arguments['proto'], arguments['model'])

    image = cv2.imread(arguments['image'])
    (height, width) = image.shape[:2]

    # PRE-PROCESSING
    # blobFromImage is a pre-processing function that subtracts mean and scales down
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)),
                                 1.0,
                                 (300, 300),
                                 (104.0, 177.0, 123.0),
                                 True)



    # DETECT FACES
    print("[INFO] Computing object detections...")
    net.setInput(blob)
    detections = net.forward()

    # DRAW FACES
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2] # The probability with detection

        if confidence > arguments['confidence']:
            box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
            (start_x, start_y, end_x, end_y) = box.astype('int')
            cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

    cv2.imshow("Output", image)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()


def detect_faces(image, confidence):
    pass
