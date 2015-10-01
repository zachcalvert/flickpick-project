# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0010_auto_20150930_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='tags',
            field=models.ManyToManyField(to='movies.Tag', null=True, blank=True),
        ),
    ]
