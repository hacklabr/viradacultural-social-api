# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from viradacultural_social_api.views import MinhaViradaView


urlpatterns = [

    # Django Admin
    url(r'^admin/', include(admin.site.urls)),

    # Criar ou adicionar evento à minha virada
    # Ler minha virada
    # fbuser_uid
    # return:
    # {"uid":"10206883790036210",
    # "picture":"https:\/\/fbcdn-profile-a.akamaihd.net\/hprofile-ak-xaf1\/v\/t1.0-1\/p200x200\/527684_4234015251569_1294087152_n.jpg?oh=d944d82092c8d09b3d636add756fdf16&oe=562FB9AD&__gda__=1446226107_f38b23393059eb9161502de807e699a4",
    # "events":[2274,1182,1180,967,973],
    # "name":"Virgilio N Santos",
    # "modalDismissed":false}
    url(r'^api/minhavirada/', MinhaViradaView.as_view()),

    # Ver amigos que vão em um evento
    # method: GET
    # get parameters: fbuser_uid, oauth_token, event_id (optional)
    # return: JSON: {

    # Salvar posição do usuário
    # method: POST
    # data: JSON {fb_user_id:  "asd3qd", oauth_token: "sfdasasdf", position: "POINT(lat,long)"}

    # Pegar posição dos amigos
    # method: GET
    # get parameters: fb_user_id, oauth_token
    # return: JSON: {fb_friend_uid1: "lat,long", fb_friend_uid1: "lat,long", ...}

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
