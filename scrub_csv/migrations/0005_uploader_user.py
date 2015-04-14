# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scrub_csv', '0004_auto_20150414_0309'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploader',
            name='user',
            field=models.OneToOneField(default=0, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
