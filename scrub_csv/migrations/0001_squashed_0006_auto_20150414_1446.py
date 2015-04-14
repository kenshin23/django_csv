# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [(b'scrub_csv', '0001_initial'), (b'scrub_csv', '0002_auto_20150414_0300'), (b'scrub_csv', '0003_auto_20150414_0301'), (b'scrub_csv', '0004_auto_20150414_0309'), (b'scrub_csv', '0005_uploader_user'), (b'scrub_csv', '0006_auto_20150414_1446')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('user', models.OneToOneField(default=0, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='uploader',
            field=models.ForeignKey(to='scrub_csv.Uploader'),
        ),
        migrations.RenameField(
            model_name='document',
            old_name='file_name',
            new_name='csvfile',
        ),
        migrations.RemoveField(
            model_name='document',
            name='csvfile',
        ),
        migrations.AddField(
            model_name='document',
            name='file_name',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
