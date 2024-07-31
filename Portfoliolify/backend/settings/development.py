from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': config('SQL_DATABASE'),
        # 'USER': config('SQL_USER'),
        # 'PASSWORD': config('SQL_PASSWORD'),
        # 'HOST': config('SQL_HOST'),
        # 'PORT': config('SQL_PORT'),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # 'LOCATION': 'redis://redis:6379/1',
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}