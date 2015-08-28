# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20150827_1748'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='director',
            new_name='directors',
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='genre',
            new_name='genres',
        ),
    ]
