# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS += ['djcelery']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '123'
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION':  '%s:%s' % ('127.0.0.1', 6379),
    },
}

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'files', 'media')


THUMBNAIL_DEBUG = True


# Celery settings

BROKER_URL = 'redis://127.0.0.1/1'

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_RESULT_BACKEND = 'djcelery.backends.cache:CacheBackend'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

CELERY_TIMEZONE = 'UTC'

import djcelery
djcelery.setup_loader()