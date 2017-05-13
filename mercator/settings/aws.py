from mercator.settings.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ('www.geopuzzle.org', 'geopuzzle.org', '52.213.89.12', '127.0.0.1')
MEDIA_ROOT = '../upload'
MEDIA_URL = '/media/'

DATABASES['default']['HOST'] = 'geopuzzle.cdihw1nj9qxz.eu-west-1.rds.amazonaws.com'
CACHES['default']['LOCATION'] = 'redis://geopuzzle.hxeqqh.0001.euw1.cache.amazonaws.com:6379/1'
SESSION_REDIS_HOST = 'geopuzzle.hxeqqh.0001.euw1.cache.amazonaws.com'
THUMBNAIL_REDIS_HOST = 'geopuzzle.hxeqqh.0001.euw1.cache.amazonaws.com'
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [('geopuzzle.hxeqqh.0001.euw1.cache.amazonaws.com', 6379)]
SETTINGS_MODULE = 'mercator.settings.aws'

LOGGING["loggers"] = {
    "django": {
        "handlers": ["file"],
        "level": "ERROR",
        "propagate": True
    }
}

#SECURE_SSL_REDIRECT = True
#SESSION_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_HTTPONLY = True
#CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 1
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

AWS_ACCESS_KEY_ID = 'AKIAIY6XKWEZVZ5A67DQ'
AWS_SECRET_ACCESS_KEY = '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'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
THUMBNAIL_STORAGE = DEFAULT_FILE_STORAGE

AWS_S3_SECURE_URLS = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_USE_SSL = True

AWS_REGION = 'eu-west-1'
AWS_STORAGE_BUCKET_NAME = 'geo-puzzle'
STATIC_URL = 'https://{}.s3.amazonaws.com/static/'.format(AWS_STORAGE_BUCKET_NAME)

THUMBNAIL_DUMMY_SOURCE = '{}images/world/default_%(width)s.png'.format(STATIC_URL)
