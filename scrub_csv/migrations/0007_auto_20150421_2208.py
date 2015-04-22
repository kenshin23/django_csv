# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrub_csv', '0006_auto_20150416_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='found_file',
            field=models.FileField(default='', upload_to=b'uploads/%Y/%m/%d', verbose_name=b'found records'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='not_found_file',
            field=models.FileField(default='', upload_to=b'uploads/%Y/%m/%d', verbose_name=b'not found records'),
            preserve_default=False,
        ),
    ]
