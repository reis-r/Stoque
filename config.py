DEBUG = True

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

MONGODB_SETTINGS = {
    'db': 'stoque',
    'host': 'mongodb://127.0.0.1:27017/stoque'
}

CSRF_ENABLE = True

CSRF_SESSION_KEY = 'secret'

SECRET_KEY = 'secret'
