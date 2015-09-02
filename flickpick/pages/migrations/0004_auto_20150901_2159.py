# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150831_2122'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ['name']},
        ),
        migrations.RemoveField(
            model_name='page',
            name='default_for_platform',
        ),
        migrations.AddField(
            model_name='movieswidget',
            name='source_year',
            field=models.CharField(max_length=4, null=True, blank=True),
        ),
    ]
