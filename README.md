# Face Detection

This is a simple Flask app that uses built-in deep learning `dnn` module in `opencv` to detect faces. The app is hosted on AWS and you can check it out here.

## USAGE

To use the app, go to the link provided above. The homepage looks something like this - 

Enter confidence value between `0.0` and `0.99` (inclusive) and then upload an image.

The app will then return an image with bounding-boxes around the face(s) with respective confidence level (if they are above the input threshold value). See the example below