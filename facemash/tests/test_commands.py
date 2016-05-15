# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from io import BytesIO
import os
import shutil

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils.six import StringIO
from django.core.files.storage import FileSystemStorage

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


def test_text_file():
    """
    Create text file.
    """
    io = BytesIO()
    io.write(b'test')
    text_file = InMemoryUploadedFile(
        io, None, 'test.txt', 'text', 'utf-8', None)
    text_file.seek(0)

    return text_file


class LoadimageTest(TestCase):
    def setUp(self):
        # Create test directory.
        self.test_dir = 'test'
        makedirs(self.test_dir)
        self.test_fs = FileSystemStorage(location=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @override_settings(DEFAULT_FILE_STORAGE='facemash.storage.TestStorage')
    def test_command_output_pick_folder(self):
        """
        Test loadimage command when pick folder.
        """
        out = StringIO()

        # Run command with empty direction of images.
        call_command('loadimage', folder=self.test_dir, stdout=out)

        # Stdout write: 'Media direction is empty'.
        self.assertIn(
            'Directory is empty %s' % self.test_dir,  out.getvalue())

        # Create image file.
        self.test_fs.save('test.jpg', test_image())

        # Run command with one image in direction.
        call_command('loadimage', folder=self.test_dir, stdout=out)

        # Delete image file and test directory.
        self.test_fs.delete('test.jpg')

        # Check that file load to database.
        person = Person.objects.get(name='test')
        self.assertEqual(person.image.name, 'uploads/test.jpg')

    @override_settings(DEFAULT_FILE_STORAGE='facemash.storage.TestStorage')
    def test_command_output_folder_has_text_and_image_files(self):
        """
        Test loadimage command when pick folder.
        """
        out = StringIO()

        # Run command with empty direction of images.
        call_command('loadimage', folder=self.test_dir, stdout=out)

        # Stdout write: 'Media direction is empty'.
        self.assertIn(
            'Directory is empty %s' % self.test_dir,  out.getvalue())

        # Create image files.
        self.test_fs.save('test_text.txt', test_text_file())
        self.test_fs.save('test.jpg', test_image())

        # Run command with one image in direction.
        call_command('loadimage', folder=self.test_dir, stdout=out)

        # Delete image file and test directory.
        self.test_fs.delete('test_text.txt')

        # Check that file load to database.
        person_list = Person.objects.all()
        self.assertEqual(len(person_list), 1)
        person = person_list[0]
        self.assertEqual(person.image.name, 'uploads/test.jpg')

    @override_settings(DEFAULT_FILE_STORAGE='facemash.storage.TestStorage')
    def test_command_output_folder_has_text_file_with_image_extension(self):
        """
        Test loadimage command when pick folder.
        """
        out = StringIO()

        # Run command with empty direction of images.
        call_command('loadimage', folder=self.test_dir, stdout=out)

        # Stdout write: 'Media direction is empty'.
        self.assertIn(
            'Directory is empty %s' % self.test_dir,  out.getvalue())

        # Create image file.
        self.test_fs.save('test_text.jpg', test_text_file())

        # Run command with one image in direction.
        call_command('loadimage', folder=self.test_dir, stdout=out)

        # Delete image file and test directory.
        self.test_fs.delete('test_text.txt')

        # Check that file load to database.
        person = Person.objects.count()
        self.assertEqual(person, 0)
