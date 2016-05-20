# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import imghdr

from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.conf import settings

from facemash.models import Person


try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


images_dir = os.path.join(
    settings.MEDIA_ROOT, getattr(settings, 'IMG_DIR', 'images'))


class Command(BaseCommand):
    help = 'Load images from directory to database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--folder',
            action='store',
            dest='folder',
            default=images_dir,
            help='Load images from the pick folder, default\
                  that is "images" folder in settings.MEDIA_ROOT directory')

    def handle(self, *args, **options):
        path = options['folder']

        # Check whether the folder.
        try:
            image_dir = os.listdir(path)
        except FileNotFoundError as err:
            raise CommandError(err)

        count = 0
        for file in image_dir:
            path_file = os.path.join(path, file)

            if os.path.isfile(path_file) and (
                    imghdr.what(path_file) is not None):
                with open(path_file, 'rb') as f:
                    Person.objects.create(image=File(f))
                count += 1
        if not count:
            self.stdout.write(
                self.style.ERROR('Directory is empty %s' % path))
        else:
            self.stdout.write(
                self.style.SUCCESS('Successfully loaded %s images' % count))
