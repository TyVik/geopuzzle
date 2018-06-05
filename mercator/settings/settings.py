import os
import raven

from django.utils.translation import ugettext_lazy as _

DEBUG = TEMPLATE_DEBUG = True

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..')
LOG_DIR = os.path.join(BASE_DIR, 'logs')
GEOJSON_DIR = os.path.join(BASE_DIR, 'geojson')

SECRET_KEY = os.environ.get('SECRET_KEY')
GOOGLE_KEY = os.environ.get('GOOGLE_KEY')
OSM_KEY = os.environ.get('OSM_KEY')
OSM_URL = 'https://wambachers-osm.website/boundaries/exportBoundaries?cliVersion=1.0&cliKey={key}&exportFormat=json&exportLayout=levels&exportAreas=land&union=false&selected={id}'

ALLOWED_HOSTS = ('127.0.0.1',)
INTERNAL_IPS = ALLOWED_HOSTS

WSGI_APPLICATION = 'mercator.wsgi.application'
ROOT_URLCONF = 'mercator.urls'
SETTINGS_EXPORT = ['RAVEN_CONFIG', 'STATIC_URL', 'GOOGLE_KEY']

# region BASE
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.humanize',
    'django.contrib.sitemaps',

    'common',
    'floppyforms',
    'sorl.thumbnail',
    'channels',
    'admirarchy',
    'social_django',
    'raven.contrib.django.raven_compat',
    'awesome_avatar',

    'users',
    'maps',
    'puzzle',
    'quiz',
]

MIDDLEWARE = [
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# if DEBUG:
#     MIDDLEWARE.append('common.middleware.CORSMiddleware')

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'django_settings_export.settings_export',
        ],
        'debug': DEBUG
    },
}]

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_USER_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'ATOMIC_REQUESTS': True,
    }
}
# endregion

# region CACHES & SESSIONS & WEB-SOCKETS
REDIS_HOST = os.environ.get('REDIS_HOST')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": 'redis://{}:6379/1'.format(REDIS_HOST),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.lzma.LzmaCompressor",
            "SOCKET_CONNECT_TIMEOUT": 2,
            "SOCKET_TIMEOUT": 2,
        }
    }
}
CACHE_MIDDLEWARE_SECONDS = 36000
CACHE_MIDDLEWARE_KEY_PREFIX = 'site'

SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_DB = 2
SESSION_REDIS_HOST = REDIS_HOST

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(REDIS_HOST, 6379)],
        },
        'ROUTING': 'mercator.routing.channels',
    }
}
# endregion

# region LOGGING
GIT_REVISION = raven.fetch_git_sha(BASE_DIR)[:8]
RAVEN_CONFIG = {
    'dsn': os.environ.get('RAVEN_DSN'),
    'release': GIT_REVISION,
}
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)s %(message)s"
        },
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            'filename': os.path.join(LOG_DIR, 'django.errors'),
            "formatter": "verbose",
            "level": "INFO",
            "maxBytes": 10485760,
            'backupCount': 10,
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
        "null": {
            "class": "logging.NullHandler",
        },
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': [],
        },
        'django.request': {
            'level': 'ERROR'  # only because noisy 404
        },
        "django.security.DisallowedHost": {
            "handlers": [],
            "propagate": False
        },
    }
}
# endregion

# region LOCALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)
ALLOWED_LANGUAGES = tuple([x for x, _ in LANGUAGES])
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
# endregion

# region STATIC & MEDIA
STATIC_URL = '/static/'
STATICFILES_DIRS = ['static']

MEDIA_URL = '/upload/'
MEDIA_ROOT = 'upload'

THUMBNAIL_DUMMY = True
THUMBNAIL_DUMMY_SOURCE = '/static/images/world/default_%(width)s.png'
THUMBNAIL_DUMMY_RATIO = 1
THUMBNAIL_REDIS_HOST = REDIS_HOST
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'

JSON_EDITOR_JS = 'https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/4.2.1/jsoneditor.js'
JSON_EDITOR_CSS = 'https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/4.2.1/jsoneditor.css'
# endregion

# region USER & SOCIAL AUTH
AUTH_USER_MODEL = 'users.User'
LOGOUT_REDIRECT_URL = 'index'
AUTH_PASSWORD_VALIDATORS = []
AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
SOCIAL_AUTH_USER_MODEL = 'users.User'
SOCIAL_AUTH_SANITIZE_REDIRECTS = True
SOCIAL_AUTH_LOGIN_ERROR_URL = '/error/'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '800277227889-g5173earcca4k7spc50k9n0t31o3fhek.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('SOCIAL_GOOGLE_SECRET')
SOCIAL_AUTH_FACEBOOK_KEY = '1273749826026102'
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('SOCIAL_FACEBOOK_SECRET')
SOCIAL_AUTH_VK_OAUTH2_KEY = '5849697'
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.environ.get('SOCIAL_VK_SECRET')
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email, first_name, last_name, locale, picture'
}
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'public_profile']
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']
SOCIAL_AUTH_VK_OAUTH2_EXTRA_DATA = []  # https://vk.com/dev/users.get
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'users.pipeline.user_details'
)
AWESOME_AVATAR = {
    'select_area_width': 250,
}
# endregion
