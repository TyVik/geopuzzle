from mercator.settings.settings import *

DEBUG = False

MEDIA_ROOT = '../upload'
MEDIA_URL = '/media/'

MIDDLEWARE = ('django.middleware.cache.UpdateCacheMiddleware', *MIDDLEWARE,
              'django.middleware.cache.FetchFromCacheMiddleware')

SESSION_REDIS_HOST = REDIS_HOST
THUMBNAIL_REDIS_HOST = REDIS_HOST
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'

LOGGING["loggers"] = {
    "django": {
        "handlers": ["file"],
        "level": "ERROR",
        "propagate": True
    },
    'raven': {
        'level': 'DEBUG',
        'handlers': ['console'],
        'propagate': False,
    },
    'sentry.errors': {
        'level': 'DEBUG',
        'handlers': ['console'],
        'propagate': False,
    }
}
LOGGING['handlers'].update({
    'sentry': {
            'level': 'INFO',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
})
LOGGING.update({
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
})

#SECURE_SSL_REDIRECT = True
#SESSION_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_HTTPONLY = True
#CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 1
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

CLOUDFRONT_DOMAIN = 'd3mrnwpzw0hkkh.cloudfront.net'
DEFAULT_FILE_STORAGE = 'mercator.storages.CloudFrontStorage'
THUMBNAIL_STORAGE = DEFAULT_FILE_STORAGE

AWS_S3_SECURE_URLS = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_USE_SSL = True

AWS_REGION = 'eu-west-1'
AWS_STORAGE_BUCKET_NAME = 'geo-puzzle'
STATIC_URL = f'https://{CLOUDFRONT_DOMAIN}/static/'

THUMBNAIL_DUMMY_SOURCE = f'{STATIC_URL}images/world/default_%(width)s.png'
