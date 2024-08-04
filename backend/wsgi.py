"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from decouple import config

settings_file = config("DJANGO_SETTINGS")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_file)

application = get_wsgi_application()
