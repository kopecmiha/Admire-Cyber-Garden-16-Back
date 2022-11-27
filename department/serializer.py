from rest_framework import serializers
from .models import Department
from accounts.serializer import UserSerializer


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Department
        fields = "id", "title", "chief", "head_department", "members"


class DepartmentViewSerializer(serializers.ModelSerializer):

    members = serializers.SerializerMethodField("resolve_members")
    member_count = serializers.SerializerMethodField("resolve_member_count")


    def resolve_member_count(self, department):
        return department.members.count()

    def resolve_members(self, department):
        if self.context.get("resolve_members"):
            return UserSerializer(instance=department.members, many=True).data
        return []

    class Meta(object):
        model = Department
        fields = "id", "title", "chief", "head_department", "members", "member_count"
        extra_kwargs = {"id": {"read_only": True}, "chief": {"read_only": True}, "member_count": {"read_only": True}}

    chief = UserSerializer()
