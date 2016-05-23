# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
 

class Migration(migrations.Migration):

    def load_data(self, orm):
        "Load initial data: admin user and person data."
        from django.core.management import call_command
        call_command("loaddata", "facemash_data.json")

    dependencies = [
        ('facemash', '0002_auto_20160522_1016'),
    ]

    operations = [
        migrations.RunPython(load_data),
    ]
