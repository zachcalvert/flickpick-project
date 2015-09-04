# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20150902_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.SlugField(choices=[(b'featured', b'Featured'), (b'all', b'All'), (b'user_reel', b'User Reel'), (b'romance', b'Romance'), (b'drama', b'Drama'), (b'horror', b'Horror'), (b'recommended', b'Recommended')], blank=True, help_text=b'indicates that this page will be returned when a special API endpoint is hit', null=True),
        ),
    ]
