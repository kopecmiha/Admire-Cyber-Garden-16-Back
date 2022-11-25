from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = "first_name", "last_name", "patronymic", "email", 'password', "uuid",
        extra_kwargs = {'uuid': {'read_only': True}}


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = "email", 'password', "username"