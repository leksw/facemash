# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
from io import BytesIO

from django.test import TestCase, override_settings
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


class PersonModelTest(TestCase):
    @override_settings(DEFAULT_FILE_STORAGE='facemash.storage.TestStorage')
    def setUp(self):
        random.seed(1)
        self.person_one = Person.objects.create(
            name='Aruny', image=test_image())
        self.person_two = Person.objects.create(
            name='Vika', image=test_image())

    def test_person_default_fields(self):
        """
        Make shure that every person has default value field 'k' is 24,
        and field 'ratio' is 0.
        """
        # Take all person.
        all_person = Person.objects.all()

        # check that its field 'k' is 24.
        self.assertEqual(len(all_person), 2)
        self.assertEqual(int(all_person[0].k), 24)
        self.assertEqual(int(all_person[0].rate), 0)
        self.assertEqual(int(all_person[1].k), 24)
        self.assertEqual(int(all_person[1].rate), 0)

    def test_person_score_method(self):
        """
        Test method score that take other instance of Person (unselected),
        and calculate new ratio person.
        """
        self.assertEqual(self.person_one.rate, 0)
        self.assertEqual(self.person_two.rate, 0)
        self.assertEqual(self.person_one.k, 24)

        # Applay score method person_one.
        self.person_one.score(self.person_two)

        # Take person_one from db.
        person_win = Person.objects.get(id=self.person_one.id)

        # Check that ratio is 24:
        #  expected_p1 = 1/(1+10**((ratio_p2-ratio_p1)/400))
        #  new_ratio_p1 = ratio_p1 + p1.k*(1-expected_p1)

        self.assertEqual(self.person_one.k, 24)
        self.assertEqual(person_win.rate, 12.0)
