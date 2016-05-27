# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import *


DEBUG = False

ALLOWED_HOSTS = ['aleks.pythonanywhere.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aleks$facemash',
        'USER': 'aleks',
        'PASSWORD': 'facemash1',
        "HOST": 'aleks.mysql.pythonanywhere-services.com'
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '/tmp/memcached.sock',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'files', 'media')


# os.environ['MEMCACHE_SERVERS'] = 'pub-memcache-10305.us-east-1-2.4.ec2.garantiadata.com:10305' 
# os.environ['MEMCACHE_USERNAME'] = 'aleks'
# os.environ['MEMCACHE_PASSWORD'] = 'hjlbjy12'