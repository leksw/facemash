# _*_ coding: utf-8 _*_
from __future__ import unicode_literals

import random
import os

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class RandomQuerySet(models.QuerySet):
    def two_random(self):
        list_id = self.values_list('id', flat=True)
        if len(list_id) < 2:
            return self.none()
        first_id = random.choice(list_id)
        list_id2 = list_id.exclude(id=first_id)
        second_id = random.choice(list_id2)
        return self.filter(id__in=[first_id, second_id])


@python_2_unicode_compatible
class Person(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploads/')
    rate = models.FloatField(default=0)
    k = models.PositiveSmallIntegerField(default=24)

    objects = RandomQuerySet.as_manager()

    def __str__(self):
        return self.name

    def score(self, competitor):
        """
        Take competitor and calculates a new rating person that is winer.s
        """
        if not isinstance(competitor, Person) or self.id == competitor.id:
            raise ValueError
        expected_rate = 1/(1+10**((competitor.rate-self.rate)/400))
        self.rate = self.rate + self.k*(1-expected_rate)
        self.save()
        return self.rate

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = os.path.splitext(os.path.split(self.image.path)[-1])[0]
        super(Person, self).save(*args, **kwargs)
