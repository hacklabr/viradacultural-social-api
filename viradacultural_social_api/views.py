from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FbUser, Event
from .serializer import FbUserSerializer
from rest_framework import permissions
import facebook


class MinhaViradaView(APIView):

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        fb_user_uid = request.query_params.get('uid')
        if fb_user_uid:
            try:
                fb_user = FbUser.objects.get(uid=fb_user_uid)
                serializer = FbUserSerializer(fb_user)
                return Response(serializer.data)
            except FbUser.DoesNotExist:
                return Response('{}')
        else:
            return Response('{}')

    def post(self, request):
        fb_user_uid = request.data.get('uid')
        data = request.data
        data['fb_user_uid'] = fb_user_uid
        if fb_user_uid:
            fb_user, _ = FbUser.objects.get_or_create(uid=fb_user_uid)
            serializer = FbUserSerializer(fb_user, data=data)
            if serializer.is_valid():
                serializer.save()
                events = request.data.get('events')
                for event in events:
                    Event.objects.get_or_create(event_id=event, fb_user=fb_user)
            return Response('{status: success}')
        else:
            return Response('{status: fail}')


# class FriendsOnEventViewSet(APIView):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = FbUser.objects.all()
#     serializer_class = UserSerializer
#
#     def get(self, request, *args, **kwargs):
#         fb_user_id = request.query_params('uid')
#         oauth_access_token = request.query_params('fbtoken')
#         graph = facebook.GraphAPI(oauth_access_token)
#         profile = graph.get_object("me")
#         friends = graph.get_connections("me", "friends")
#
#
# class FriendsPositionsView(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = FbUser.objects.all()
#     serializer_class = UserSerializer
#
#     def get(self, request, *args, **kwargs):
#         fb_user_id = request.query_params('uid')
#         oauth_access_token = request.query_params('fbtoken')
#         graph = facebook.GraphAPI(oauth_access_token)
#         profile = graph.get_object("me")
#         friends = graph.get_connections("me", "friends")
#         from django.contrib.gis.geos import fromstr
#         pnt = fromstr('POINT(-90.5 29.5)', srid=4326)

