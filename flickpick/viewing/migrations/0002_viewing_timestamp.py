# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('viewing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewing',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 27, 23, 39, 16, 944603, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
