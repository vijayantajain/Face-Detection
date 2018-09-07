# Face Detection

This is a simple Flask app that uses built-in deep learning `dnn` module in `opencv` to detect faces. The app is hosted on Heroku and you can check it out [here](https://opencv-face-detection.herokuapp.com/).

## USAGE

To use the app, go to the link provided above.

Enter confidence value between `0.0` and `0.99` (inclusive) and then upload an image.

The app will then return an image with bounding-boxes around the face(s) with respective confidence level (if they are above the input threshold value).

## HOW IT WORKS

We use the `dnn` module in the `opencv` library to use the deep learning model for face-detection.

1. First, we pre-process the uploaded image using `blobFromImage` method in the `dnn` module.

2. Then, we feed forward the blob to the network and get detections. Detections returned by the model are a 4-D Tensor with the following dimensions `[img, channels, num_detections, property]`. The neural network is created from the `protxt.txt` and `.caffemodel` files. This code uses `res10_300x300_ssd_iter_140000` caffe model obtained from [here](https://www.pyimagesearch.com/2018/02/26/face-detection-with-opencv-and-deep-learning/)

3. Then we draw rectangles of only those detections whose probability is greater or equal to the input-threshold value and also write the probability.

## INSTALLATION

To install on your system follow the instructions below

### Prequisites

Have `python` > 3.5 installed and preferably use virtual environment.

### Steps

1. Clone the repository

    `git clone https://github.com/vijayantajain/face_detection.git`

2. Create and activate the virtual environment

    `python3 -m venv <name-of-env>`

    On Windows

    `.\<name-of-env>\Scripts\activate`

    On Linux

    `source bin/activate`

3. Install dependencies

    `python3 -m pip install -r requirements.txt`

4. Change host

    In `run.py` change host from `0.0.0.0` to `127.0.0.1`.

5. Change environment variable to `DEBUG`

    On Windows Powershell

    `$env:FLASK_ENV = "debug"`

    On Linux

    `export FLASK_ENV=debug`

6. Run the application

    Run `python run.py`

    And then type `127.0.0.1:5000` in the browser!