# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrub_csv', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file_name',
            field=models.FileField(upload_to=b''),
        ),
    ]
