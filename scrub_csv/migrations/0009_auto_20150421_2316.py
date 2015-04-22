# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrub_csv', '0008_auto_20150421_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='found_file',
            field=models.FileField(upload_to=b'downloads/%Y/%m/%d', null=True, verbose_name=b'found records', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='not_found_file',
            field=models.FileField(upload_to=b'downloads/%Y/%m/%d', null=True, verbose_name=b'not found records', blank=True),
        ),
    ]
