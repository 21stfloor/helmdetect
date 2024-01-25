# imageupload/firebase_init.py

import firebase_admin
from firebase_admin import credentials
from pathlib import Path
import os
import json

BASE_DIR = Path(__file__).resolve().parent.parent


cred = credentials.Certificate(os.path.join(BASE_DIR, 'helmetdetect2-firebase-adminsdk-r98rq-7b231713df.json'))  # Replace with your service account key path
firebase_admin.initialize_app(cred, {
    'storageBucket': 'helmdetect.appspot.com'  # Replace with your Firebase Storage bucket URL
})