# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image


def test_image(title):
    """
    Created test image file
    """
    im = Image.new(mode='RGB', size=(200, 200))  # create a new image using PIL
    im_io = BytesIO()  # a StringIO object for saving image
    im.save(im_io, 'JPEG')  # save the image to im_io
    im_io.seek(0)  # seek to the beginning

    image = InMemoryUploadedFile(
        im_io, None, title, 'image/jpeg', im_io.getvalue(), None
    )

    return image


def test_file(title):
    """
    Create text file.
    """
    io = BytesIO()
    io.write(b'test')
    text_file = InMemoryUploadedFile(
        io, None, title, 'text', 'utf-8', None)
    text_file.seek(0)

    return text_file


def makedirs(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == 17:
            # Dir already exists. No biggie.
            pass
