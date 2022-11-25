from rest_framework import serializers
from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Department
        fields = "title", "chief", "head_department"

