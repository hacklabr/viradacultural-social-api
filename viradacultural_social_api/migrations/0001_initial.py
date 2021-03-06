# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('event_id', models.IntegerField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='FbUser',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('uid', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=512)),
                ('picture', models.CharField(max_length=2048)),
                ('position', django.contrib.gis.db.models.fields.PointField(srid=4326, blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='fb_user',
            field=models.ForeignKey(related_name='events', to='viradacultural_social_api.FbUser'),
        ),
    ]
