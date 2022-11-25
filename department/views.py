from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from department.serializer import DepartmentSerializer, DepartmentViewSerializer
from department.models import Department


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
        serializer = DepartmentSerializer(data=serializer_data, partial=1)
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
        serializer = DepartmentViewSerializer(instance=departments, many=True)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)



