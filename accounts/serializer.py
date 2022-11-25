from rest_framework import serializers
from .models import User
from .utils import get_jwt_token


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField('get_jwt')

    def get_jwt(self, user):
        token = ""
        if self.context.get("is_auth"):
            token = get_jwt_token(user)
        return token

    class Meta(object):
        model = User
        fields = "first_name", "last_name", "patronymic", "email", "uuid", "token", "avatar", "grade", "specialization", "date_birthday",
        extra_kwargs = {'uuid': {'read_only': True}, "token": {'read_only': True}}


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = "email", 'password', "username", "first_name", "last_name", "patronymic",
