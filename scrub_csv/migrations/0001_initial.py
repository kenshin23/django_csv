# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=200)),
                ('upload_date', models.DateTimeField(verbose_name=b'date uploaded')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('row', models.PositiveIntegerField()),
                ('doc_key', models.CharField(max_length=200)),
                ('doc_value', models.CharField(default=b'', max_length=200)),
                ('document', models.ForeignKey(to='scrub_csv.Document')),
            ],
        ),
        migrations.CreateModel(
            name='Uploader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('is_active', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='uploader',
            field=models.ForeignKey(to='scrub_csv.Uploader'),
        ),
    ]
