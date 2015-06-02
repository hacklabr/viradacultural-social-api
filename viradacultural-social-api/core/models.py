# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.db import models
# from django.utils.translation import ugettext_lazy as _


class MinhaVirada(models.Model):

    user = models.CharField(max_length=256)

    # def __unicode__(self):
    #     return self.username
