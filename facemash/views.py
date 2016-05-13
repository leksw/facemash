# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.core import serializers

from .models import Person


def home(request):
    return render(request, 'home.html')


def top(request):
    top_person = Person.objects.order_by('-rate')[:10]
    context = {'top_person': top_person}
    return render(request, 'top.html', context)


def home_request(request):
    if request.is_ajax():
        if request.method == 'POST':
            two_random_person = Person.objects.two_random()
            top_person = Person.objects.order_by('-rate')[:4]

            two_random = serializers.serialize("json", two_random_person)
            top = serializers.serialize("json", top_person)

            return JsonResponse({'two': two_random, 'top': top}, safe=False)

    return HttpResponseBadRequest('Error request')


def score(request):
    if request.is_ajax():
        if request.method == 'POST':
            win_id = request.POST['win_id']
            loser_id = request.POST['loser_id']

            win = Person.objects.get(id=int(win_id))
            loser = Person.objects.get(id=int(loser_id))

            rate = win.score(loser)

            return JsonResponse({win_id: rate})

    return HttpResponseBadRequest('Error request')
