from rest_framework import serializers
from .models import FbUser, Event


class EventsListingField(serializers.RelatedField):
    def to_representation(self, value):
        return value.event_id


class FbUserSerializer(serializers.ModelSerializer):

    position_timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M', required=False)
    events = EventsListingField(many=True, read_only=True)
    lat = serializers.SerializerMethodField()
    long = serializers.SerializerMethodField()

    class Meta:
        model = FbUser

    @staticmethod
    def get_lat(obj):
        if obj.position:
            return str(obj.position.y)

    @staticmethod
    def get_long(obj):
        if obj.position:
            return str(obj.position.x)


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
