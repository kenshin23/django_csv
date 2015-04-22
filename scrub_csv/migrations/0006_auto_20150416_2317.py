# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrub_csv', '0005_auto_20150414_2104'),
    ]

    operations = [
        migrations.CreateModel(
            name='Row',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permanent', models.BooleanField(default=True)),
                ('document', models.ForeignKey(to='scrub_csv.Document')),
            ],
        ),
        migrations.RemoveField(
            model_name='record',
            name='document',
        ),
        migrations.AlterField(
            model_name='record',
            name='row',
            field=models.ForeignKey(to='scrub_csv.Row'),
        ),
    ]
