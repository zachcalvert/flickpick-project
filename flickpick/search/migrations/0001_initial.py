# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('display', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromotedSearchResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('banner', models.ForeignKey(to='display.BannerWidget', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
