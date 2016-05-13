# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.conf import settings

from facemash.models import Person


class Command(BaseCommand):
    help = 'Load images from directory to database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            action='store',
            dest='path',
            default=settings.MEDIA_ROOT,
            help='Load images from direction of this path')

    def handle(self, *args, **options):
        path = options['path']

        # Check if pick directory than add it to path.
        if path != settings.MEDIA_ROOT:
            path = os.path.join(settings.MEDIA_ROOT, path)

        # Check whether the folder.
        try:
            image_dir = os.listdir(path)
        except FileNotFoundError as err:
            raise CommandError(err)

        count = 0
        for file in image_dir:
            path_file = os.path.join(path, file)
            if os.path.isfile(path_file):
                with open(path_file, 'rb') as f:
                    Person.objects.create(image=File(f))
                count += 1
        if not count:
            self.stdout.write(
                self.style.ERROR('Media direction is empty %s' % path))
        else:
            self.stdout.write(
                self.style.SUCCESS('Successfully loaded %s images' % count))
