from .settings import *

DEBUG = False
MEDIA_ROOT = '../upload'
MEDIA_URL = '/media/'

LOGGING["loggers"] = {
    "django": {
        "handlers": ["file"],
        "level": "ERROR",
        "propagate": True
    }
}
