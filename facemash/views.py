# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import Person


def home(request):
    two_random_person = Person.objects.two_random()
    top_person = Person.objects.order_by('-rate')[:4]
    context = {'two_random_person': two_random_person,
               'top_person': top_person}
    return render(request, 'home.html', context)
