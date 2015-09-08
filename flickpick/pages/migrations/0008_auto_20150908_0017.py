# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_auto_20150907_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='adcarouselitem',
            name='sort_order',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='adgroupitem',
            name='sort_order',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='movieswidget',
            name='source_year',
            field=models.CharField(blank=True, max_length=4, null=True, choices=[(b'2015', b'2015'), (b'2014', b'2014'), (b'2013', b'2013'), (b'2012', b'2012'), (b'2011', b'2011'), (b'2010', b'2010')]),
        ),
    ]
