# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0011_auto_20151001_0019'),
        ('pages', '0010_auto_20150923_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='movieswidget',
            name='source_tag',
            field=models.ForeignKey(blank=True, to='movies.Tag', null=True),
        ),
    ]
