# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrub_csv', '0005_uploader_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='csvfile',
        ),
        migrations.RemoveField(
            model_name='uploader',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='uploader',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='uploader',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='uploader',
            name='password',
        ),
        migrations.RemoveField(
            model_name='uploader',
            name='username',
        ),
        migrations.AddField(
            model_name='document',
            name='file_name',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='record',
            name='doc_value',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
