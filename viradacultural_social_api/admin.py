# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin

from .models import FbUser, Event


# admin.site.register(FbUser)


@admin.register(FbUser)
class FbUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Event)
