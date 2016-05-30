# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import json

from django.test import TestCase, override_settings
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.contrib.auth import get_user_model

from facemash.models import Person
from .utils_test import test_image


User = get_user_model()


def create_persons(num):
    rate = 0
    for i in range(num):
        name = 'test%s' % i
        image = 'img%s.jpg' % i
        rate += 1
        Person.objects.create(name=name, image=image, rate=rate)


class HomePageTest(TestCase):
    @override_settings(DEFAULT_FILE_STORAGE='facemash.storage.TestStorage')
    def setUp(self):
        random.seed(1)
        self.person_one = Person.objects.create(
            name='Aruny', image=test_image('aruny.jpg'))
        self.person_two = Person.objects.create(
            name='Vika', image=test_image('vika.jpg'))
        self.user = User.objects.create_user(username='test', password='12345')

        # Clear cache.
        cache.clear()

    def tearDown(self):
        Person.objects.all().delete()

    def test_home_page_template(self):
        response = self.client.get(reverse('home'))

        # Check template and content text.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn(b"Who's hotter? Click to choose!", response.content)

    @override_settings(DEFAULT_FILE_STORAGE='facemash.storage.TestStorage')
    def test_home_page_three_person_in_db(self):
        """
        Make sure that home_ajax view return only two person.
        """
        # Add three person.
        self.person_three = Person.objects.create(
            name='Dasha', image=test_image('dasha.jpg'))

        response = self.client.get(reverse('home-ajax'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Check content data.
        self.assertIn(b"Aruny", response.content)
        self.assertIn(b"Vika", response.content)

    @override_settings(DEFAULT_FILE_STORAGE='facemash.storage.TestStorage')
    def test_home_page_four_or_more_person_in_db(self):
        """
        Make sure that home_ajax view return only four person.
        """
        # Add four and five person.
        self.person_four = Person.objects.create(
            name='Lena', image=test_image('lena.jpg'))
        self.person_five = Person.objects.create(
            name='Katy', image=test_image('katy.jpg'))

        response = self.client.get(reverse('home-ajax'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Check content data.
        self.assertIn(b"Aruny", response.content)
        self.assertIn(b"Vika", response.content)
        self.assertNotIn(b"Dahsa", response.content)
        self.assertIn(b"Lena", response.content)
        self.assertIn(b"Katy", response.content)

    def test_home_page_one_person_in_db(self):
        """
        Make sure that home_ajax view return two = []
        when one person is in db.
        """
        # Delete one person.
        person = Person.objects.first()
        person.delete()

        response = self.client.get(reverse('home-ajax'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Check content data.
        self.assertIn(b'"two": []', response.content)

    def test_home_page_empty_person_db(self):
        """
        Make sure that home_ajax view return two = []
        when person db is empty.
        """
        # Delete all persons.
        person = Person.objects.all()
        person.delete()

        response = self.client.get(reverse('home-ajax'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Check content data.
        self.assertIn(b'"two": []', response.content)

    def test_home_page_with_login_user(self):
        """
        Make shure that home page has 'Upload images' link when
        user logging into the site.
        """
        response = self.client.get(reverse('home'))

        # Home page don't has link 'Upload images'.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertNotIn(b"Upload images", response.content)

        # Logging into the site.
        self.client.login(username=self.user.username, password='12345')

        response = self.client.get(reverse('home'))

        # Now page has link 'Upload images'.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn(b"Upload images", response.content)

    def test_top_page(self):
        """
        Make shure that top page views not more than 10 items,
        and order by rate field.
        """
        # Create 10 person.
        create_persons(10)

        # Go to top page.
        response = self.client.get(reverse('top'))

        test9 = Person.objects.get(name='test9')
        test0 = Person.objects.get(name='test0')
        aruny = Person.objects.get(id=self.person_one.id)

        # Now top page has only 10 created person.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'top.html')

        self.assertEqual(test9.rate, 10)
        self.assertEqual(test0.rate, 1)
        self.assertEqual(aruny.rate, 0)
        self.assertIn(b"test9", response.content)
        self.assertIn(b"test0", response.content)
        self.assertNotIn(b"Aruny", response.content)
        self.assertNotIn(b"Vika", response.content)

    def test_home_ajax_not_ajax_request(self):
        """
        Make shure that home_ajax return error: "Person could not be returned,
        if request isn't ajax.
        """
        # Send not ajax request.
        response = self.client.post(reverse('home-ajax'))

        self.assertEqual(
            'Person could not be returned.',
            json.loads(response.content.decode("utf-8"))['errors'])

    def test_score_not_ajax_request(self):
        """
        Make shure that score return error: "Person is not be scored,
        if request isn't ajax.
        """
        # Send not ajax request.
        response = self.client.get(reverse('score'))

        self.assertEqual(
            'Person is not be scored.',
            json.loads(response.content.decode("utf-8"))['errors'])

    def test_upload_image_not_post_request(self):
        """
        Make shure that upload_image return error: "Image has not be uploaded,
        if request isn't POST.
        """
        # Send not ajax request.
        response = self.client.get(reverse('upload-images'))

        self.assertEqual(
            'Image has not be uploaded.',
            json.loads(response.content.decode("utf-8"))['errors'])

    def test_upload_image(self):
        """
        Make shure that upload_image return success message when loaded images.
        """
        # Send not ajax request.
        response = self.client.post(
            reverse('upload-images'),
            {'quantity': 2,
             'file[0]': test_image('upload1.jpg'),
             'file[1]': test_image('upload2.jpg')},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(
            'Files are loaded.',
            json.loads(response.content.decode("utf-8"))['success'])

    def test_score_ajax_request(self):
        """
        Make shure that score view is scored persons
        which id have been given and return rate of winner.
        """
        # Send not ajax request.

        response = self.client.post(
            reverse('score'),
            {'win_id': self.person_one.id, 'loser_id': self.person_two.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        winner = Person.objects.get(id=self.person_one.id)
        self.assertEqual(
            winner.rate,
            json.loads(
                response.content.decode("utf-8"))[str(self.person_one.id)])

    def test_score_ajax_request_taken_id_same_person(self):
        """
        Make shure that score view returns error
        if have been taken two identical id which belong one person.
        """
        # Send not ajax request.
        with self.assertRaises(ValueError) as cm:
            self.client.post(
                reverse('score'),
                {'win_id': self.person_one.id, 'loser_id': self.person_one.id},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        the_exception = cm.exception
        self.assertIn(
            'Argument of the score method do not must be',
            the_exception.args[0])
