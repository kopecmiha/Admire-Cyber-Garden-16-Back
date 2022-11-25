import re

import jwt
from django.contrib.auth import user_logged_in
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import jwt_payload_handler

from accounts.models import User
from department.serializer import DepartmentSerializer
from department.models import Department
from main import settings


class CreateDepartment(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        request = request.data
        serializer = DepartmentSerializer(data=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Department successfully created"}, status=status.HTTP_201_CREATED)


class UpdateDepartment(APIView):
    permission_classes = (IsAdminUser,)

    def put(self, request):
        serializer_data = request.data
        serializer = DepartmentSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)


class DeleteDepartment(APIView):
    permission_classes = (IsAdminUser,)

    def delete(self, request):
        department_id = request.data.get("id")
        department_filter = Department.objects.filter(pk=department_id)
        department_filter.delete()
        return Response(status=status.HTTP_200_OK)



class GetDepartments(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(instance=departments, many=True)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)



