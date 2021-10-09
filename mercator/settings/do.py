from mercator.settings.settings import *  # lgtm [py/polluting-import]

DEBUG = False
ALLOWED_HOSTS = ('geopuzzle.org', '206.81.16.242')

MEDIA_ROOT = '../upload'
MEDIA_URL = '/media/'

LOGGING['loggers']['fetch_region'] = {
    'handlers': ['console'],
    'level': 'DEBUG'
}

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_HTTPONLY = False
SECURE_HSTS_SECONDS = 180 * 24 * 60 * 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# region S3 & CLOUDFRONT
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION = 'eu-west-1'
AWS_STORAGE_BUCKET_NAME = 'geo-puzzle'
AWS_DEFAULT_ACL = 'public-read'

DEFAULT_FILE_STORAGE = 'mercator.storages.CloudFrontStorage'
THUMBNAIL_STORAGE = DEFAULT_FILE_STORAGE

CLOUDFRONT_DOMAIN = 'd2nepmml5nn7q0.cloudfront.net'
STATIC_URL = 'https://{}/static-{}/'.format(CLOUDFRONT_DOMAIN, GIT_REVISION)
THUMBNAIL_DUMMY_SOURCE = '{}images/world/default_%(width)s.png'.format(STATIC_URL)
# endregion
