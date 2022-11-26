from rest_framework import serializers
from .models import User
from .utils import get_jwt_token
from department.models import Department


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField("get_jwt")
    department = serializers.SerializerMethodField("resolver_department")
    uuid = serializers.SerializerMethodField("username_as_uuid")

    def username_as_uuid(self, user):
        return user.username

    def resolver_department(self, user):
        user_department = Department.objects.filter(members__in=[user.id]).first()
        if user_department:
            chief = User.objects.filter(pk=user_department.chief.id)
            if chief:
                chief = chief.first()
                chief_name = (chief.last_name or "") + " " + (chief.first_name or "")
                chief_dict = {"chief_id": chief.pk, "chief_name": chief_name}
            else:
                chief_dict = {}
            department_dict = {"id": user_department.id, "title": user_department.title}
            department_dict.update(chief_dict)
            return department_dict
        return {}

    def get_jwt(self, user):
        token = ""
        if self.context.get("is_auth"):
            token = get_jwt_token(user)
        return token

    class Meta(object):
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "patronymic",
            "email",
            "token",
            "avatar",
            "grade",
            "specialization",
            "date_birthday",
            "department",
            "uuid",
            "fact1",
            "fact2",
            "fact3",
            "city",
            "online",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
            "token": {"read_only": True},
            "department": {"read_only": True},
        }


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = (
            "email",
            "password",
            "username",
            "first_name",
            "last_name",
            "patronymic",
        )
