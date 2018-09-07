"""Module to run the app"""

import os

from face_detector import app

PORT = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=PORT)
