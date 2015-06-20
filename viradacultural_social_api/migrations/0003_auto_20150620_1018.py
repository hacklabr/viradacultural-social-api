# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('viradacultural_social_api', '0002_auto_20150616_1838'),
    ]

    operations = [
        migrations.CreateModel(
            name='FbUserPositionHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('uid', models.CharField(max_length=256)),
                ('position_timestamp', models.DateTimeField(null=True, blank=True)),
                ('position', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='fbuser',
            name='map_picture',
            field=models.CharField(max_length=2048, null=True, blank=True),
        ),
    ]
