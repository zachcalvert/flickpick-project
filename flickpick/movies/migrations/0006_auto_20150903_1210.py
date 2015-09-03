# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_auto_20150827_2327'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='actor',
            name='name',
        ),
        migrations.RemoveField(
            model_name='director',
            name='name',
        ),
        migrations.RemoveField(
            model_name='writer',
            name='name',
        ),
        migrations.AddField(
            model_name='actor',
            name='person',
            field=models.ForeignKey(default=1, to='movies.Person'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='director',
            name='person',
            field=models.ForeignKey(default=1, to='movies.Person'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='writer',
            name='person',
            field=models.ForeignKey(default=1, to='movies.Person'),
            preserve_default=False,
        ),
    ]
