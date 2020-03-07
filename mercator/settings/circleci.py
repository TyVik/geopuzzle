from .settings import *


STATIC_ROOT = 'collected_static'

LOGGING['handlers'].pop('file', None)
LOGGING['handlers'].pop('commands', None)
LOGGING['loggers'].pop('commands', None)
LOGGING['loggers'].pop('wambachers', None)
