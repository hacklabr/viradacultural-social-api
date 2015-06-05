from rest_framework import serializers
from .models import FbUser, Event


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FbUser


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event