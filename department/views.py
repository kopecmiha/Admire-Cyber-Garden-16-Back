from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from department.serializer import DepartmentSerializer, DepartmentViewSerializer
from department.models import Department
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

import random
User = get_user_model()


class CreateDepartment(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        request = request.data
        request["chief"] = User.objects.get(username=request.pop("chief")).id
        request["members"] = list(User.objects.filter(username__in=request.pop("members")).values_list("id", flat=True))
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
        params = request.query_params
        resolve_members = params.get("members", False)
        departments = Department.objects.all()
        serializer = DepartmentViewSerializer(instance=departments, many=True, context={"resolve_members": resolve_members})
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)


class GetDepartment(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, department_id):
        try:
            params = request.query_params
            resolve_members = params.get("members", False)
            department = Department.objects.get(pk=department_id)
            serializer = DepartmentViewSerializer(instance=department, context={"resolve_members": resolve_members})
            response = serializer.data
        except ObjectDoesNotExist:
            return Response({"message": "Department not found"}, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_200_OK)


class SetDepartment(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        department_dict = {"Веб разработка":  Department.objects.create(title="Веб разработка"),
                           "Мобильная разработка": Department.objects.create(title="Мобильная разработка"),
                           "QA":Department.objects.create(title="QA"),
                           "Диджитал контент":Department.objects.create(title="Диджитал контент"),
                           "HR":Department.objects.create(title="HR"),
                           "Коммерческий отдел":Department.objects.create(title="Коммерческий отдел")}

        users = User.objects.all()
        for user in users:
            if "-разработчик" in user.specialization.lower() or "веб-аналитик" in user.specialization.lower():
                department_dict["Веб разработка"].members.add(user)
            elif "мобильный разработчик" in user.specialization.lower():
                department_dict["Мобильная разработка"].members.add(user)
            elif "бухгалтер" in user.specialization.lower():
                department_dict["Коммерческий отдел"].members.add(user)
            elif user.specialization.lower() in ["дизайнер", "маркетолог", "контент-менеджер"]:
                department_dict["Диджитал контент"].members.add(user)
            elif user.specialization.lower() in ["инженер техподдержки", "тестировщик", ]:
                department_dict["QA"].members.add(user)
            elif user.specialization.lower() in ["инженер техподдержки", "тестировщик", "системный администратор"]:
                department_dict["QA"].members.add(user)
            elif user.specialization.lower() == "менеджер по персоналу":
                department_dict["HR"].members.add(user)
            elif user.specialization.lower() in ["руководитель проектов", "системный аналитик"] :
                random.choice([department_dict["Веб разработка"], department_dict["Мобильная разработка"]]).members.add(user)
        for department in department_dict.values():
            department.chief = random.choice(department.members.filter(Q(grade="SENIOR") | Q(grade="NULL")))
            department.save()

        return Response("ok", status=status.HTTP_200_OK)
