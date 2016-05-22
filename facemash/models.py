# _*_ coding: utf-8 _*_
from __future__ import unicode_literals

import random
import os

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.query import EmptyQuerySet
from django.db.models import F

from sorl.thumbnail.shortcuts import get_thumbnail


class RandomQuerySet(models.QuerySet):
    def two_random(self):
        list_id = self.values_list('id', flat=True)
        if len(list_id) < 2:
            return self.none()
        first_id = random.choice(list_id)
        list_id_without_first_id = list_id.exclude(id=first_id)
        second_id = random.choice(list_id_without_first_id)
        return self.filter(id__in=[first_id, second_id])

    def two_random_with_thumbnail(self, size):
        if isinstance(self.two_random(), EmptyQuerySet):
            return []

        first, second = self.two_random().values()
        first_person, second_person = (
            self.get(id=first['id']), self.get(id=second['id']))

        first.update(
            {'thumbnail': first_person.get_thumbnail(size)})
        second.update(
            {'thumbnail': second_person.get_thumbnail(size)})

        return [first, second]

    def all_with_thumbnail(self, order, quantity, size):
        all_person = self.order_by(order)[:quantity].values()

        person_with_thumbnail = []
        for person in all_person:
            person.update(
                {'thumbnail': self.get(id=person['id']).get_thumbnail(size)})
            person_with_thumbnail.append(person)

        return person_with_thumbnail


@python_2_unicode_compatible
class Person(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploads/')
    rate = models.FloatField(default=0)
    k = models.PositiveSmallIntegerField(default=24)
    win = models.PositiveIntegerField(default=0)
    lose = models.PositiveIntegerField(default=0)

    objects = RandomQuerySet.as_manager()

    def __str__(self):
        return self.name

    def score(self, competitor):
        """
        Take competitor and calculates a new rating person that is winer.
        """
        if not isinstance(competitor, Person) or self.id == competitor.id:
            raise ValueError

        expected_rate = 1/float(1+10**((competitor.rate-self.rate)/400))
        self.rate = self.rate + self.k*(1-expected_rate)
        self.win = F('win') + 1
        self.save()

        competitor.lose = F('lose') + 1
        competitor.save()

        return self.rate

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = os.path.splitext(os.path.split(self.image.path)[-1])[0]

        # Object is possibly being updated, if so, clean up.
        self._remove_on_image_update()
        super(Person, self).save(*args, **kwargs)

    def get_thumbnail(self, size):
        img = self.image
        return get_thumbnail(img, '%(size)ix%(size)i' % {'size': size}).url

    def get_thumbnail_300(self):
        return self.get_thumbnail(300)

    def get_thumbnail_75(self):
        return self.get_thumbnail(75)

    def _remove_on_image_update(self):
        try:
            # Is the object in the database yet?
            obj = Person.objects.get(id=self.id)
        except Person.DoesNotExist:
            # Object is not in db, nothing to worry about.
            return
        # Is the save due to an update of the actual image file?
        if obj.image and self.image and obj.image != self.image:
            # Delete the old image file from the storage
            obj.image.delete()
