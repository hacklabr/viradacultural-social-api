from rest_framework import serializers
from .models import FbUser, Event


class EventsListingField(serializers.RelatedField):
    def to_representation(self, value):
        return value.event_id


class FbUserSerializer(serializers.ModelSerializer):

    position_timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    events = EventsListingField(many=True, read_only=True)
    lat = serializers.SerializerMethodField()
    long = serializers.SerializerMethodField()

    class Meta:
        model = FbUser

    @staticmethod
    def get_lat(obj):
        return str(obj.position.x)

    @staticmethod
    def get_long(obj):
        return str(obj.position.y)


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
