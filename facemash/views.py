# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseBadRequest

from .models import Person


def home(request):
    return render(request, 'home.html')


def top(request):
    top_person = Person.objects.order_by('-rate')[:10]
    context = {'top_person': top_person}
    return render(request, 'top.html', context)


def home_ajax(request):
    if request.is_ajax():
        two_random_thumbnail = Person.objects.two_random_with_thumbnail(300)
        top_thumbnail = Person.objects.all_with_thumbnail('-rate', 4, 75)

        return JsonResponse(
            {'two': two_random_thumbnail,
             'top': top_thumbnail})

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
