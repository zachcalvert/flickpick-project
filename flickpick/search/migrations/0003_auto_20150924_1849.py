# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_auto_20141204_1547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promotedsearchresult',
            name='banner',
        ),
        migrations.DeleteModel(
            name='PromotedSearchResult',
        ),
    ]
