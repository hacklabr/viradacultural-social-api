# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.db import models
# from django.utils.translation import ugettext_lazy as _


class FbUser(models.Model):

    fb_user_uid = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    picture = models.CharField(max_length=512)

    position = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Event(models.Model):
    id_event = fb_user_uid = models.CharField(max_length=128)
    fb_user = models.ForeignKey(User)
