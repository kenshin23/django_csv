# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrub_csv', '0002_auto_20150414_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='file_name',
        ),
        migrations.AddField(
            model_name='document',
            name='csvfile',
            field=models.FileField(default='', upload_to=b'uploads/%Y/%m/%d'),
            preserve_default=False,
        ),
    ]
