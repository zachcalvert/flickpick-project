# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewing', '0003_viewing_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewing',
            name='rating',
            field=models.DecimalField(null=True, max_digits=2, decimal_places=1, blank=True),
        ),
    ]
