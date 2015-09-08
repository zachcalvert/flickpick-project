# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_auto_20150903_2106'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pagetowidget',
            options={'ordering': ['page', 'sort_order']},
        ),
        migrations.AddField(
            model_name='pagetowidget',
            name='sort_order',
            field=models.IntegerField(default=0),
        ),
    ]
