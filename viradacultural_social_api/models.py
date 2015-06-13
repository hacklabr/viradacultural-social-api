# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
# from django.db import models
from django.contrib.gis.db import models
# from django.utils.translation import ugettext_lazy as _


class FbUser(models.Model):

    uid = models.CharField(max_length=256)
    name = models.CharField(max_length=512)
    picture = models.CharField(max_length=2048)

    position = models.PointField()
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Event(models.Model):
    event_id = models.IntegerField(db_index=True)
    fb_user = models.ForeignKey(FbUser, related_name='events', db_index=True)

    def __unicode__(self):
        return str(self.event_id) + ' - ' + self.fb_user.name

    def __str__(self):
        return str(self.event_id) + ' - ' + self.fb_user.name