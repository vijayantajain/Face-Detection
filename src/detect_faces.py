"""Module for detecting faces"""

import argparse
import imghdr
import os
from os import path

CWD = os.getcwd()

def create_parser():
    """Argument Parser"""
    parser = argparse.ArgumentParser(description=
                                     "CMD line arguments for the image")

    parser.add_argument('--image', '-i', type=str,
                        dest='image',
                        help='Path file to the image',
                        required=True)

    parser.add_argument('--confidence', type=float,
                        dest='confidence',
                        help='Confidence level threshold above which the app will draw rectangles',
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
    if not path.isfile(arguments['image']):
        raise AssertionError('Path to the image is invalid')

    if imghdr.what(arguments['image']) not in ['png', 'jpeg']:
        raise AssertionError('Image is neither png or jpeg')

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

if __name__ == '__main__':
    main()
