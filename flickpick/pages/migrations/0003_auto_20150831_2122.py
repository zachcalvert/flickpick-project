# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20150831_2028'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adcarouselitem',
            options={'verbose_name': 'ad', 'verbose_name_plural': 'ads'},
        ),
        migrations.AlterModelOptions(
            name='adgroupitem',
            options={'verbose_name': 'ad', 'verbose_name_plural': 'ads'},
        ),
        migrations.AlterModelOptions(
            name='pagetowidget',
            options={'ordering': ['page']},
        ),
        migrations.RemoveField(
            model_name='adgroupitem',
            name='sort_order',
        ),
        migrations.RemoveField(
            model_name='pagetowidget',
            name='sort_order',
        ),
        migrations.AlterUniqueTogether(
            name='adcarouselitem',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='adcarouselitem',
            name='sort_order',
        ),
    ]
