# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from io import BytesIO
import os
import shutil

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils.six import StringIO
from django.core.files.storage import default_storage

from PIL import Image

from facemash.models import Person


PHOTO_FILE = 'photo.jpg'


def makedirs(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == 17:
            # Dir already exists. No biggie.
            pass


def test_image():
    """
    Created test image file
    """
    im = Image.new(mode='RGB', size=(200, 200))  # create a new image using PIL
    im_io = BytesIO()  # a StringIO object for saving image
    im.save(im_io, 'JPEG')  # save the image to im_io
    im_io.seek(0)  # seek to the beginning

    image = InMemoryUploadedFile(
        im_io, None, PHOTO_FILE, 'image/jpeg', im_io.getvalue(), None
    )

    return image


class LoadimageTest(TestCase):
    @override_settings(DEFAULT_FILE_STORAGE='facemash.storage.TestStorage')
    def test_command_output(self):
        """
        Test loadimage command.
        """
        out = StringIO()

        # Create test directory.
        test_dir = os.path.join(default_storage.location, 'test')
        makedirs(test_dir)

        # Run command with empty direction of images.
        call_command('loadimage', path='test', stdout=out)

        # Stdout write: 'Media direction is empty'.
        self.assertIn('Media direction is empty', out.getvalue())

        # Load image file.
        default_storage.save('test/test.jpg', test_image())

        # Run command with one image in direction.
        call_command('loadimage', path='test', stdout=out)

        # Delete image file and test directory.
        default_storage.delete('test/test.jpg')
        shutil.rmtree(test_dir)
        # Check that file load to database.
        person = Person.objects.get(name='test')
        self.assertEqual(person.image.name, 'uploads/test.jpg')
