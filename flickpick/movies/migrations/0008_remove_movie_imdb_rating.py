# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_auto_20150904_1506'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='imdb_rating',
        ),
    ]
