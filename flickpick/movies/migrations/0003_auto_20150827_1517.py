# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_movie_poster_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='imdb_rating',
            field=models.DecimalField(default=0, max_digits=2, decimal_places=1),
        ),
    ]
