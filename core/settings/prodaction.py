# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import *
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)
 
SECRET_KEY = get_env_variable('SECRET_KEY')


DEBUG = False


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'files', 'media')