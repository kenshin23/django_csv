# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrub_csv', '0003_auto_20150414_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='upload_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'date uploaded'),
        ),
    ]
