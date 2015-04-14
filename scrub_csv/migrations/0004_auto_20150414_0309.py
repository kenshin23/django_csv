# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrub_csv', '0003_auto_20150414_0301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='doc_value',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
