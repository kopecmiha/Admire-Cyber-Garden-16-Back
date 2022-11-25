from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from department.serializer import DepartmentSerializer, DepartmentViewSerializer
from department.models import Department
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
User = get_user_model()


class CreateDepartment(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        request = request.data
        serializer = DepartmentSerializer(data=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Department successfully created"}, status=status.HTTP_201_CREATED)


class AddToDepartment(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        user_id = request.data.get("user_id")
        department_id = request.data.get("department_id")
        try:
            user_to_add = User.objects.get(pk=user_id)
            department_to_update = Department.objects.get(pk=department_id)
            department_to_update.members.add(user_to_add)
            department_to_update.save()
        except Exception as e:
            print(e)
            return Response({"message": "Department or user not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)


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
        serializer = DepartmentViewSerializer(instance=departments, many=True)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)


class GetDepartment(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, department_id):
        try:
            department = Department.objects.get(pk=department_id)
            serializer = DepartmentViewSerializer(instance=department)
            response = serializer.data
        except ObjectDoesNotExist:
            return Response({"message": "Department not found"}, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_200_OK)


