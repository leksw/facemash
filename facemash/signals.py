# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Person


@receiver(pre_delete, sender=Person, dispatch_uid='delete_image_file')
def delete_image_file(sender, **kwargs):
    kwargs['instance'].image.delete()
