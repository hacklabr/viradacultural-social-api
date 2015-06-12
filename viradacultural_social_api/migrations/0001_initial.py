# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('event_id', models.IntegerField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='FbUser',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('uid', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=512)),
                ('picture', models.CharField(max_length=2048)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='fb_user',
            field=models.ForeignKey(related_name='events', to='viradacultural_social_api.FbUser'),
        ),
    ]
