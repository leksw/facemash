# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.flatpages import views as fpviews

from facemash import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^about/$', fpviews.flatpage, {'url': '/about/'}, name='about'),
    url(r'^contact/$', fpviews.flatpage, {'url': '/contact/'}, name='contact'),

    url(r'^$', views.home, name='home'),
    url(r'^top/$', views.top, name='top'),
    url(r'^score/$', views.score, name='score'),
    url(r'^home_request/$', views.home_ajax, name='home-ajax'),
    url(r'^upload_images/$', views.upload_image, name='upload-images'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
