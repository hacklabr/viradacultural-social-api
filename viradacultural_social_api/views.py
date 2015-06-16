from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FbUser, Event
from .serializer import FbUserSerializer
from rest_framework import permissions
import facebook


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
            return Response('{status: success}')
        else:
            return Response('{status: fail}')


class FriendsOnEventsView(APIView):

    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        # fb_user_id = request.query_params.get('uid')
        oauth_access_token = request.query_params.get('oauth_token')
        # import ipdb;ipdb.set_trace()
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

