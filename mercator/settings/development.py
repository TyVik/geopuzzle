from mercator.settings.settings import *

STATIC_ROOT = 'collected_static'
ALLOWED_HOSTS = ('*',)

GDAL_LIBRARY_PATH = '/usr/lib/libgdal.so'
GEOS_LIBRARY_PATH = '/usr/lib/libgeos_c.so.1'
RAVEN_CONFIG = {}

LOGGING['loggers']['django.db.backends'].update({
    'handlers': ['console'],
    'level': 'ERROR'
})
LOGGING['loggers']['fetch_region'] = {
    'handlers': ['console'],
    'level': 'DEBUG'
}
