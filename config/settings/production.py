# -*- coding: utf-8 -*-
'''
Production Configurations

- Use djangosecure
- Use Amazon's S3 for storing static files and uploaded media
- Use sendgrid to send emails
- Use MEMCACHIER on Heroku
'''
from __future__ import absolute_import, unicode_literals

from .common import *

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANO_SECRET_KEY not in os.environ
SECRET_KEY = env("DJANGO_SECRET_KEY")

if env('FORCE_SCRIPT_NAME', default=False):
    FORCE_SCRIPT_NAME = env('FORCE_SCRIPT_NAME')

# django-secure
# ------------------------------------------------------------------------------
# INSTALLED_APPS += ("djangosecure", )
#
# MIDDLEWARE_CLASSES = (
#     # Make sure djangosecure.middleware.SecurityMiddleware is listed first
#     'djangosecure.middleware.SecurityMiddleware',
# ) + MIDDLEWARE_CLASSES

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]
# END SITE CONFIGURATION

INSTALLED_APPS += ("gunicorn", )


if env.bool("DJANGO_CORS", False):
    # django-cors-headers
    MIDDLEWARE_CLASSES += ('corsheaders.middleware.CorsMiddleware',)
    INSTALLED_APPS += ('corsheaders', )
    CORS_ORIGIN_ALLOW_ALL = True


# Static Assests
# ------------------------


# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
DATABASES['default'] = env.db("DATABASE_URL")

# CACHING
# ------------------------------------------------------------------------------
# try:
#     # Only do this here because thanks to django-pylibmc-sasl and pylibmc
#     # memcacheify is painful to install on windows.
#     # See: https://github.com/rdegges/django-heroku-memcacheify
#     from memcacheify import memcacheify
#     CACHES = memcacheify()
# except ImportError:
#     CACHES = {
#         'default': env.cache_url("DJANGO_CACHE_URL", default="memcache://127.0.0.1:11211"),
#     }

# Your production stuff: Below this line define 3rd party library settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
    )
}

MAP_PICTURES_PATH = env('MAP_PICTURES_PATH')
MAP_PICTURES_MASK_FILE_PATH = env('MAP_PICTURES_MASK_FILE_PATH')
MAP_PICTURES_BASE_URL = env('MAP_PICTURES_BASE_URL')
MAP_PICTURES_SIZE = env('MAP_PICTURES_SIZE')