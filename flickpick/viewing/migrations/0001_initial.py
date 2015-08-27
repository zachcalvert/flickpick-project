# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_movie_poster_url'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Viewing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('movie', models.ForeignKey(related_name='viewers', to='movies.Movie')),
                ('user', models.ForeignKey(related_name='seen_movies', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'viewing',
                'verbose_name': 'Viewing',
                'verbose_name_plural': 'Viewing',
            },
        ),
        migrations.AlterUniqueTogether(
            name='viewing',
            unique_together=set([('user', 'movie')]),
        ),
    ]
