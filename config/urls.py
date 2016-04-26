# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from viradacultural_social_api.views import MinhaViradaView, FriendsOnEventsView, FriendsPositionsView


urlpatterns = [

    # Django Admin
    url(r'^%sadmin/' % getattr(settings, 'URL_PREFIX'),
        include(admin.site.urls)),
    url(r'^%s(api/)?minhavirada/' % getattr(settings, 'URL_PREFIX'),
        MinhaViradaView.as_view()),
    url(r'^%s(api/)?friendsevents' % getattr(settings, 'URL_PREFIX'),
        FriendsOnEventsView.as_view()),
    url(r'^%s(api/)?friendspositions' % getattr(settings, 'URL_PREFIX'),
        FriendsPositionsView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', 'django.views.defaults.bad_request'),
        url(r'^403/$', 'django.views.defaults.permission_denied'),
        url(r'^404/$', 'django.views.defaults.page_not_found'),
        url(r'^500/$', 'django.views.defaults.server_error'),
    ]
