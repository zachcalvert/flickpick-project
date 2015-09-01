# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adcarouselitem',
            name='image_aspect_ratio',
        ),
        migrations.RemoveField(
            model_name='adcarouselitem',
            name='image_avg_color',
        ),
        migrations.RemoveField(
            model_name='adcarouselitem',
            name='image_timestamp',
        ),
        migrations.RemoveField(
            model_name='adgroupitem',
            name='image_aspect_ratio',
        ),
        migrations.RemoveField(
            model_name='adgroupitem',
            name='image_avg_color',
        ),
        migrations.RemoveField(
            model_name='adgroupitem',
            name='image_timestamp',
        ),
        migrations.RemoveField(
            model_name='bannerwidget',
            name='image_aspect_ratio',
        ),
        migrations.RemoveField(
            model_name='bannerwidget',
            name='image_avg_color',
        ),
        migrations.RemoveField(
            model_name='bannerwidget',
            name='image_timestamp',
        ),
        migrations.RemoveField(
            model_name='bannerwidget',
            name='portrait_alignment',
        ),
    ]
