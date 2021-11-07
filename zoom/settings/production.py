"""
settings required for production environment
"""
from zoom.settings.base import *
import os 

DEBUG = False
ALLOWED_HOSTS = ["*"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["PRODUCTION_NAME"],
        "HOST": os.environ["PRODUCTION_HOST"],
        "USER": os.environ["PRODUCTION_USER"],
        "PASSWORD": os.environ["PRODUCTION_PASSWORD"],
    }
}