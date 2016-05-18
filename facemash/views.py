# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

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


def home_ajax(request):
    if request.is_ajax():
        two_random_person = Person.objects.two_random()
        thumbl_persons = []
        for person in enumerate(two_random_person.values()):
            person[1].update(
                {'thumbnail': two_random_person[person[0]].get_thumbnail_300()})
            thumbl_persons.append(person[1])

        top_person = Person.objects.order_by('-rate')[:4]
        thumbl_top = []
        for top in enumerate(top_person.values()):
            top[1].update(
                {'thumbnail': top_person[top[0]].get_thumbnail_75()})
            thumbl_top.append(top[1])
        # two_random = serializers.serialize("json", two_random_person)
        # top = serializers.serialize("json", top_person)

        return JsonResponse({'two': thumbl_persons, 'top': thumbl_top})

    return HttpResponseBadRequest(
        content=json.dumps({"errors": "Person could not be returned."}),
        content_type="application/json")


def score(request):
    if request.is_ajax():
        if request.method == 'POST':
            win_id = request.POST['win_id']
            loser_id = request.POST['loser_id']

            win = Person.objects.get(id=int(win_id))
            loser = Person.objects.get(id=int(loser_id))

            rate = win.score(loser)

            return JsonResponse({win_id: rate})

    return HttpResponseBadRequest(
        content=json.dumps({'errors': 'Person is not be scored.'}),
        content_type="application/json")


def upload_image(request):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity')[0])
        for q in range(quantity):
            file = "file[%s]" % q
            Person.objects.create(image=request.FILES[file])

        return JsonResponse({'success': 'Files are loaded.'})

    return HttpResponseBadRequest(
        content=json.dumps({'errors': 'Person is not be scored.'}),
        content_type="application/json")
