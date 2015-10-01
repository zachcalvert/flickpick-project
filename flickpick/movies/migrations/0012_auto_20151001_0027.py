# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0011_auto_20151001_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='tags',
            field=models.ManyToManyField(to='movies.Tag'),
        ),
    ]
