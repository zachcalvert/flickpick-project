# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotedsearchresult',
            name='banner',
            field=models.ForeignKey(default=1, to='display.BannerWidget'),
            preserve_default=False,
        ),
    ]
