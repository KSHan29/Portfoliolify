from .base import *
import dj_database_url
from decouple import config
import os
import django_heroku

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd68f1ks81h3j9m',
        'USER': 'u8quio4oiifnfh', 
        'PASSWORD': 'p8d734cc0908c54cbc4a77c1e59c7c23e263d0bc6a66c2f6724cf36bd7657aa70', 
        'HOST': 'c3nv2ev86aje4j.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com', 
        'PORT': '5432', 
    }
}

REDIS_URL = os.getenv('REDISCLOUD_URL')
print(REDIS_URL)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,  # Prevents cache failures from affecting your app
        }
    }
}

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

django_heroku.settings(locals())