# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100)),
                ('year', models.CharField(max_length=4)),
                ('released', models.DateField(null=True, blank=True)),
                ('rated', models.CharField(default=b'N/A', max_length=10)),
                ('genre', models.CharField(max_length=50)),
                ('plot', models.CharField(max_length=300, null=True, blank=True)),
                ('imdb_id', models.CharField(max_length=10)),
                ('imdb_rating', models.DecimalField(max_digits=2, decimal_places=1)),
                ('notes', models.CharField(max_length=200, null=True, blank=True)),
                ('on_netflix', models.BooleanField(default=False)),
                ('on_amazon', models.BooleanField(default=False)),
                ('on_hulu', models.BooleanField(default=False)),
                ('actors', models.ManyToManyField(to='movies.Actor')),
                ('director', models.ForeignKey(to='movies.Director')),
            ],
        ),
        migrations.CreateModel(
            name='Writer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='writers',
            field=models.ManyToManyField(to='movies.Writer'),
        ),
    ]
