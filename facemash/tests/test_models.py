# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import random

from django.test import TestCase, override_settings
from django.conf import settings

from facemash.models import Person
from .utils_test import test_image


class PersonModelTest(TestCase):
    @override_settings(DEFAULT_FILE_STORAGE='facemash.storage.TestStorage')
    def setUp(self):
        random.seed(1)
        self.person_one = Person.objects.create(
            name='Aruny', image=test_image('aruny.jpg'))
        self.person_two = Person.objects.create(
            name='Vika', image=test_image('vika.jpg'))

    def tearDown(self):
        Person.objects.all().delete()

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
        Test method score that takes other instance of Person (unselected),
        and calculate new ratio person. Also it adds 1 to win person,
        and 1 to lose other person.
        """
        self.assertEqual(self.person_one.rate, 0)
        self.assertEqual(self.person_two.rate, 0)
        self.assertEqual(self.person_one.k, 24)

        # Applay score method person_one.
        self.person_one.score(self.person_two)

        # Take person_one from db.
        person_win = Person.objects.get(id=self.person_one.id)
        person_lose = Person.objects.get(id=self.person_two.id)

        # Check that ratio is 12:
        #  expected_p1 = 1/(1+10**((ratio_p2-ratio_p1)/400))
        #  new_ratio_p1 = ratio_p1 + p1.k*(1-expected_p1).
        self.assertEqual(self.person_one.k, 24)
        self.assertEqual(person_win.rate, 12.0)

        # Now win person is 1, and other person lose is 1.
        self.assertEqual(person_win.win, 1)
        self.assertEqual(person_win.lose, 0)
        self.assertEqual(person_lose.lose, 1)
        self.assertEqual(person_lose.win, 0)

    def test_person_delete_image_file_when_delete_instance(self):
        """
        Test overrided delete Person method that delete image file,
        when delete related Person instance.
        """
        del_person = Person.objects.get(name=self.person_two.name)
        self.assertEqual(del_person.name, self.person_two.name)
        del_image_path = del_person.image.name

        # Delete test person.
        del_person.delete()

        # Now check that file 'vika.jpg' is not.
        image_path = os.path.join(
            settings.MEDIA_ROOT, del_image_path)
        self.assertTrue(not os.path.isfile(image_path))

    @override_settings(DEFAULT_FILE_STORAGE='facemash.storage.TestStorage')
    def test_person_delete_image_file_when_change_image(self):
        """
        Test overrided save Person method that delete image file,
        when change image.
        """
        change_person = Person.objects.get(name=self.person_one.name)
        old_image_path = change_person.image.name
        change_person.image = test_image('aruny_new.jpg')
        change_person.save()

        # Now check that file 'aruny.jpg' is not.
        image_path = os.path.join(
            settings.MEDIA_ROOT, old_image_path)
        self.assertTrue(not os.path.isfile(image_path))
