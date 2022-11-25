from rest_framework import serializers
from .models import Department
from accounts.serializer import UserSerializer


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Department
        fields = "title", "chief", "head_department", "members"


class DepartmentViewSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Department
        fields = "title", "chief", "head_department", "members"
        extra_kwargs = {'chief': {'read_only': True}}

    chief = UserSerializer()
    members = UserSerializer(many=True)

