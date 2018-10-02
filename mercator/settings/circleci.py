from .settings import *


STATIC_ROOT = 'collected_static'
RAVEN_CONFIG['release'] = None

GDAL_LIBRARY_PATH = '/usr/lib/libgdal.so.20'
GEOS_LIBRARY_PATH = '/usr/lib/libgeos_c.so.1'

LOGGING['handlers'].pop('file', None)
