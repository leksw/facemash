# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import shutil

from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils.six import StringIO
from django.core.files.storage import FileSystemStorage

from facemash.models import Person
from .utils_test import test_image, test_file, makedirs


class LoadimageTest(TestCase):
    def setUp(self):
        # Create test directory.
        self.test_dir = 'test'
        makedirs(self.test_dir)
        self.test_fs = FileSystemStorage(location=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        Person.objects.all().delete()

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
        self.test_fs.save('test.jpg', test_image('test.jpg'))

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
        self.test_fs.save('test_text.txt', test_file('text.txt'))
        self.test_fs.save('test.jpg', test_image('test.jpg'))

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
        self.test_fs.save('test_text.jpg', test_file('text.txt'))

        # Run command with one image in direction.
        call_command('loadimage', folder=self.test_dir, stdout=out)

        # Delete image file and test directory.
        self.test_fs.delete('test_text.txt')

        # Check that file load to database.
        person = Person.objects.count()
        self.assertEqual(person, 0)
