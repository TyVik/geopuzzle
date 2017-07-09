from mercator.settings.settings import *

DEBUG = False

ALLOWED_HOSTS = ('www.geopuzzle.org', 'geopuzzle.org', '52.213.89.12', '127.0.0.1')
MEDIA_ROOT = '../upload'
MEDIA_URL = '/media/'

MIDDLEWARE = ['django.middleware.cache.UpdateCacheMiddleware'] + MIDDLEWARE + ['django.middleware.cache.FetchFromCacheMiddleware']

REDIS_HOST = 'geopuzzle.hxeqqh.0001.euw1.cache.amazonaws.com'
DATABASES['default']['HOST'] = 'geopuzzle.cdihw1nj9qxz.eu-west-1.rds.amazonaws.com'
CACHES['default']['LOCATION'] = 'redis://{host}:6379/1'.format(host=REDIS_HOST)
SESSION_REDIS_HOST = REDIS_HOST
THUMBNAIL_REDIS_HOST = REDIS_HOST
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [(REDIS_HOST, 6379)]
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

CLOUDFRONT_DOMAIN = 'd3mrnwpzw0hkkh.cloudfront.net'
DEFAULT_FILE_STORAGE = 'mercator.storages.CloudFrontStorage'
THUMBNAIL_STORAGE = DEFAULT_FILE_STORAGE

AWS_S3_SECURE_URLS = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_USE_SSL = True

AWS_REGION = 'eu-west-1'
AWS_STORAGE_BUCKET_NAME = 'geo-puzzle'
STATIC_URL = 'https://{}/static/'.format(CLOUDFRONT_DOMAIN)

THUMBNAIL_DUMMY_SOURCE = '{}images/world/default_%(width)s.png'.format(STATIC_URL)
