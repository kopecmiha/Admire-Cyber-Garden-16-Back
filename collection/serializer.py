from rest_framework import serializers
from .models import PlayCard
from accounts.serializer import UserSerializer


class PlayCardSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = PlayCard
        fields = "owner", "person"


class PlayCardViewSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = PlayCard
        fields = "owner", "person"
        extra_kwargs = {'owner': {'read_only': True}, "person": {'read_only': True}}

    owner = UserSerializer()
    person = UserSerializer()

