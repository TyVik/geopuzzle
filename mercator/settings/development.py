from mercator.settings.settings import *

STATIC_ROOT = 'collected_static'

LOGGING['loggers']['django.db.backends'].update({
    'handlers': ['console'],
    'level': 'DEBUG'
})
