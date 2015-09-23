# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_auto_20150908_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movieswidget',
            name='source_year',
            field=models.CharField(blank=True, max_length=4, null=True, choices=[(b'2015', b'2015'), (b'2014', b'2014'), (b'2013', b'2013'), (b'2012', b'2012'), (b'2011', b'2011'), (b'2010', b'2010'), (b'2009', b'2009'), (b'2008', b'2008'), (b'2007', b'2007')]),
        ),
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.SlugField(choices=[(b'featured', b'Featured'), (b'all', b'All'), (b'user_reel', b'User Reel'), (b'genres', b'Genres'), (b'recommended', b'Recommended')], blank=True, help_text=b'indicates that this page will be returned when a special API endpoint is hit', null=True),
        ),
    ]
