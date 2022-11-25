from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = "first_name", "last_name", "patronymic", "email"
        extra_kwargs = {'password': {'write_only': True}}


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = "first_name", "last_name", "patronymic", "avatar", "status", "email", "uuid"
        extra_kwargs = {'status': {'read_only': True}, 'uuid': {'read_only': True}, "email": {'read_only': True}}
