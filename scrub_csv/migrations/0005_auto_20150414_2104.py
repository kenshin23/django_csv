# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrub_csv', '0004_auto_20150414_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='csvfile',
            field=models.FileField(upload_to=b'uploads/%Y/%m/%d', verbose_name=b'file'),
        ),
    ]
