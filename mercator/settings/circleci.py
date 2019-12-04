from .settings import *


STATIC_ROOT = 'collected_static'

LOGGING['handlers'].pop('file', None)
