# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from facemash import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^top/$', views.top, name='top'),
    url(r'^score/$', views.score, name='score'),
    url(r'^home_request/$', views.home_request, name='home-request'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
