# _*_ coding: utf-8 _*_
from __future__ import unicode_literals

from core.celery import app


@app.task(name='tasks.ex')
def test():
    print("is works!")


@app.task(name='tasks.response')
def send_response():
    print('send')
