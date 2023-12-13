from django.apps import AppConfig
from helmdect.settings import FIREBASE_CONFIG
import pyrebase

class HelmdectpagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'helmdectpages'