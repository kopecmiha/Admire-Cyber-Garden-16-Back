from rest_framework import serializers
from .models import GameSession
from accounts.serializer import UserSerializer


class GameSessionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = GameSession
        fields = "duration", "finished", "points", "game_type", "try_count"

