"""Module to run the app"""

import os

from face_detector import app

PORT = int(os.environ.get('PORT', 5000))
app.run(host='127.0.0.1', port=PORT)
