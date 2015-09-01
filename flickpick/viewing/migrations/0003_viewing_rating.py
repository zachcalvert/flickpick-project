# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewing', '0002_viewing_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewing',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
