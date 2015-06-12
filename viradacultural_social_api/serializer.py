from rest_framework import serializers
from .models import FbUser, Event


class EventsListingField(serializers.RelatedField):
    def to_representation(self, value):
        return value.event_id


class FbUserSerializer(serializers.ModelSerializer):

    events = EventsListingField(many=True, read_only=True)

    class Meta:
        model = FbUser


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
