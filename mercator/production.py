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

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 1
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
