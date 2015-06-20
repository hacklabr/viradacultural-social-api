from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.gis.geos import fromstr
from django.conf import settings
from .models import FbUser, Event, FbUserPositionHistory
from .serializer import FbUserSerializer
from PIL import Image, ImageOps
import facebook
import datetime
import urllib
import io

class MinhaViradaView(APIView):

    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        fb_user_uid = request.query_params.get('uid')
        if fb_user_uid:
            try:
                fb_user = FbUser.objects.get(uid=fb_user_uid)
                serializer = FbUserSerializer(fb_user)
                return Response(serializer.data)
            except FbUser.DoesNotExist:
                return Response('')
        else:
            return Response('')

    def post(self, request, *args, **kwargs):
        fb_user_uid = request.data.get('uid')
        data = request.data
        data['fb_user_uid'] = fb_user_uid
        if fb_user_uid:
            fb_user, _ = FbUser.objects.get_or_create(uid=fb_user_uid)
            serializer = FbUserSerializer(fb_user, data=data)
            if serializer.is_valid():
                serializer.save()
                events = request.data.get('events')
                Event.objects.filter(fb_user=fb_user).exclude(event_id__in=events).delete()
                for event in events:
                    Event.objects.get_or_create(event_id=event, fb_user=fb_user)
            else:
                return Response('{status: fail}', 400)
            return Response('{status: success}')
        else:
            return Response('{status: fail}')


class FriendsOnEventsView(APIView):

    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        # fb_user_id = request.query_params.get('uid')
        oauth_access_token = request.query_params.get('oauth_token')
        if not oauth_access_token:
            return Response('Invalid Facebook Oauth Token', 400)
        event_id = request.query_params.get('event_id')
        # TODO save friends in database
        graph = facebook.GraphAPI(oauth_access_token, version='2.3')
        friends = graph.get_connections("me", "friends", fields='id, name', limit=500)
        friend_uids = [data.get('id') for data in friends.get('data')]

        if event_id:
            events = Event.objects.filter(fb_user__uid__in=friend_uids, event_id=event_id)
            events_data = {event_id: [event.fb_user.uid for event in events]}
        else:
            events = Event.objects.filter(fb_user__uid__in=friend_uids)
            events_data = {}
            for event in events:
                fb_user_data = {'uid': event.fb_user.uid,
                               'name': event.fb_user.name,
                               'picture': event.fb_user.picture}
                if event.event_id in events_data.keys():
                    events_data[event.event_id].append(fb_user_data)
                else:
                    events_data[event.event_id] = [fb_user_data]
        return Response(events_data)


class FriendsPositionsView(APIView):

    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def _get_friends_data(oauth_access_token):
        if not oauth_access_token:
            return Response('Invalid Facebook Oauth Token', 400)
        graph = facebook.GraphAPI(oauth_access_token)
        friends = graph.get_connections("me", "friends", fields='id', limit=500)
        friend_uids = [data.get('id') for data in friends.get('data')]
        queryset = FbUser.objects.filter(uid__in=friend_uids)
        serializer = FbUserSerializer(queryset, many=True)
        return serializer.data

    @staticmethod
    def _generate_map_picture(fb_user_uid, source_picture):

        size = (settings.MAP_PICTURES_SIZE, settings.MAP_PICTURES_SIZE)
        response = urllib.request.urlopen(source_picture)
        fb_avatar = Image.open(io.BytesIO(response.read()))
        fb_avatar.resize(size, Image.NEAREST)

        mask = Image.open(settings.MAP_PICTURES_MASK_FILE_PATH).convert('L').resize(size, Image.NEAREST)

        output = ImageOps.fit(fb_avatar, size, centering=(0, 0.5))
        output.putalpha(mask)
        output.save(settings.MAP_PICTURES_PATH + '/' + fb_user_uid + '.png')

    def get(self, request, *args, **kwargs):
        fb_user_id = request.query_params.get('uid')
        oauth_access_token = request.query_params.get('oauth_token')
        if fb_user_id and oauth_access_token:
            friends_data = self._get_friends_data(oauth_access_token)
            return Response(friends_data)
        else:
            return Response('{status: fail}', 400)

    def post(self, request, *args, **kwargs):
        fb_user_uid = request.data.get('uid')
        oauth_access_token = request.data.get('oauth_token')
        latitude = request.data.get('lat')
        longitude = request.data.get('long')
        timestamp = request.data.get('position_timestamp')
        if fb_user_uid and oauth_access_token:
            try:
                fb_user = FbUser.objects.get(uid=fb_user_uid)
                fb_user.position_timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M')
                # POINT(longitude latitude)
                point_wkt = 'POINT({long} {lat})'.format(long=longitude, lat=latitude)
                fb_user.position = fromstr(point_wkt, srid=4326)
                fb_user.map_picture = settings.MAP_PICTURES_BASE_URL + '/' + fb_user_uid + '.png'
                fb_user.save()

                self._generate_map_picture(fb_user.uid, fb_user.picture)

                fb_user_rev = {
                    'uid': fb_user.uid,
                    'position': fb_user.position,
                    'position_timestamp': fb_user.position_timestamp,
                }
                FbUserPositionHistory.objects.create(**fb_user_rev)
            except FbUser.DoesNotExist:
                return Response('{status: fail}', 400)
            friends_data = self._get_friends_data(oauth_access_token)
            return Response(friends_data)
        else:
            return Response('{status: fail}', 400)
