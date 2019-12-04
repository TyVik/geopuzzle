from mercator.settings.settings import *

STATIC_ROOT = 'collected_static'
ALLOWED_HOSTS = ('*',)

LOGGING['loggers']['django.db.backends'].update({
    'handlers': ['console'],
    'level': 'ERROR'
})
LOGGING['loggers']['fetch_region'] = {
    'handlers': ['console'],
    'level': 'DEBUG'
}
