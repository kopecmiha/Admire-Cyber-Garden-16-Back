from rest_framework import serializers
from .models import GameSession
from accounts.serializer import UserSerializer


class GameSessionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = GameSession
        fields = "id", "finished", "points", "game_type", "try_count", "duration"
        extra_fields = {"id": {"read_only": True}}

