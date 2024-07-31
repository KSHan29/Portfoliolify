from .base import *
import dj_database_url
import django_heroku

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    #     # 'ENGINE': 'django.db.backends.postgresql',
    #     # 'NAME': config('SQL_DATABASE'),
    #     # 'USER': config('SQL_USER'),
    #     # 'PASSWORD': config('SQL_PASSWORD'),
    #     # 'HOST': config('SQL_HOST'),
    #     # 'PORT': config('SQL_PORT'),
    # }
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv('REDIS_URL', 'redis://localhost:6379/1'),
        # 'LOCATION': 'redis://redis:6379/1',
        # "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

django_heroku.settings(locals())
