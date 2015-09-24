# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_auto_20150922_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='bannerwidget',
            name='genre',
            field=models.OneToOneField(null=True, blank=True, to='movies.Genre'),
        ),
        migrations.AlterField(
            model_name='adcarouselitem',
            name='end_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='adcarouselitem',
            name='start_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='adgroupitem',
            name='end_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='adgroupitem',
            name='start_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.SlugField(blank=True, null=True, choices=[(b'featured', b'Featured'), (b'all', b'All'), (b'user_reel', b'User Reel'), (b'genres', b'Genres'), (b'recommended', b'Recommended')]),
        ),
        migrations.AlterField(
            model_name='widget',
            name='end_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='widget',
            name='start_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
