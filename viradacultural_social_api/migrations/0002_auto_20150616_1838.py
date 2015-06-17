# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('viradacultural_social_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fbuser',
            name='friends',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=256), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='fbuser',
            name='friends_timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fbuser',
            name='position_timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
