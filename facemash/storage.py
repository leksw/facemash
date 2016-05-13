# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.files.storage import FileSystemStorage


class TestStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=50):
        if self.exists(name):
            self.delete(name)
        return name
