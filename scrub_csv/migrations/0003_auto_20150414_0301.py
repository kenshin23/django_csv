# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrub_csv', '0002_auto_20150414_0300'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='file_name',
            new_name='csvfile',
        ),
    ]
