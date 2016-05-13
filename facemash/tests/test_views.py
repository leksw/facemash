# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
from io import BytesIO

from django.test import TestCase, override_settings
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile

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


class HomePageTest(TestCase):
    @override_settings(DEFAULT_FILE_STORAGE='facemash.storage.TestStorage')
    def setUp(self):
        random.seed(1)
        self.person_one = Person.objects.create(
            name='Aruny', image=test_image())
        self.person_two = Person.objects.create(
            name='Vika', image=test_image())

    def test_home_page_template(self):
        response = self.client.get(reverse('home'))

        # check template and content text
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn(b"Who's hotter? Click to choose!", response.content)
        self.assertIn(b"Aruny", response.content)
        self.assertIn(b"Vika", response.content)

    @override_settings(DEFAULT_FILE_STORAGE='facemash.storage.TestStorage')
    def test_home_page_three_person_in_db(self):
        """
        Make sure that home page views only two person.
        """
        # add three person
        self.person_three = Person.objects.create(
            name='Dasha', image=test_image())

        response = self.client.get(reverse('home'))

        # check template and content text
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn(b"Aruny", response.content)
        self.assertIn(b"Vika", response.content)

    @override_settings(DEFAULT_FILE_STORAGE='facemash.storage.TestStorage')
    def test_home_page_four_or_more_person_in_db(self):
        """
        Make sure that home page views only four person.
        """
        # add four and five person
        self.person_four = Person.objects.create(
            name='Lena', image=test_image())
        self.person_five = Person.objects.create(
            name='Katy', image=test_image())

        response = self.client.get(reverse('home'))

        # check template and content text
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn(b"Aruny", response.content)
        self.assertIn(b"Vika", response.content)
        self.assertNotIn(b"Dahsa", response.content)
        self.assertIn(b"Lena", response.content)
        self.assertIn(b"Katy", response.content)

    def test_home_page_one_person_in_db(self):
        """
        Make sure that home page views "Need two persons at least."
        when person db is empty.
        """
        # delete one person
        person = Person.objects.first()
        person.delete()

        response = self.client.get(reverse('home'))

        # check template and content text
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn(b"Person db is empty yet!", response.content)

    def test_home_page_empty_person_db(self):
        """
        Make sure that home page views "Person db is empty yet!"
        when person db is empty.
        """
        # delete all persons
        person = Person.objects.all()
        person.delete()

        response = self.client.get(reverse('home'))

        # check template and content text
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn(b"Person db is empty yet!", response.content)
