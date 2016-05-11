# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO
from django.core.files.storage import default_storage

from PIL import Image

from facemash.models import Person


PHOTO_FILE = 'photo.jpg'


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
    def test_command_output(self):
        out = StringIO()
        call_command('loadimage', stdout=out)
        self.assertIn('Media direction is empty', out.getvalue())

        default_storage.save(test_image())
        
        call_command('loadimage', stdout=out)
        person = Person.objects.get(image=PHOTO_FILE)
        self.assertEqual(person.image.name, PHOTO_FILE)
