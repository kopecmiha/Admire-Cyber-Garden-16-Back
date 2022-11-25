from rest_framework import serializers
from .models import User
from .utils import get_jwt_token
from department.models import Department


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField('get_jwt')
    department = serializers.SerializerMethodField("resolver_department")

    def resolver_department(self, user):
        user_department = Department.objects.filter(members__in=[user.id]).first()
        chief = User.objects.get(pk=user_department.chief.id)
        chief_name = (chief.last_name or "") + (chief.first_name or "")
        return {"id": user_department.id, "title": user_department.title, "chief_id": chief.pk, "chief_name": chief_name}

    def get_jwt(self, user):
        token = ""
        if self.context.get("is_auth"):
            token = get_jwt_token(user)
        return token

    class Meta(object):
        model = User
        fields = "first_name", "last_name", "patronymic", "email", "uuid", "token", "avatar", "grade", "specialization", "date_birthday", "department"
        extra_kwargs = {'uuid': {'read_only': True}, "token": {'read_only': True}, "department": {'read_only': True}}


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = "email", 'password', "username", "first_name", "last_name", "patronymic",
