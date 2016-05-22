# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facemash', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='lose',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='person',
            name='win',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
