import json
import re
import uuid
from functools import reduce
from operator import or_

import jwt
from django.contrib.auth import user_logged_in
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User, UserRelationship
from accounts.serializer import UserSerializer, UserCreateSerializer

allowed_fileds_to_order = [
    "email",
    "first_name",
    "last_name",
    "patronymic",
    "grade",
    "specialization",
    "random"
]

allowed_fileds_to_filter = [
    "email",
    "first_name",
    "last_name",
    "patronymic",
    "grade",
    "specialization",
]


class CreateUser(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        request = request.data
        request["username"] = uuid.uuid4()
        serializer = UserCreateSerializer(data=request)
        serializer.is_valid(raise_exception=True)
        serializer.save(password=make_password(request['password']))
        user = User.objects.get(email=serializer.data["email"])
        response = UserSerializer(user, context={"is_auth": True}).data
        user_logged_in.send(sender=user.__class__,
                            request=request, user=user)
        return Response(response, status=status.HTTP_201_CREATED)


class GetUserProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)


class UserProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        try:
            user = User.objects.get(username=id)
            serializer = UserSerializer(user)
            response = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)


class Parse(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        with open('people.json', encoding="utf8") as json_data:
            people_list = json.load(json_data)
            i = 0
            for people in people_list:
                i += 1
                last_name, first_name, patronymic = people["ФИО"].split(" ")
                grade = people["Грейд"]
                if grade == "Джуниор":
                    grade = "JUNIOR"
                if grade == "Мидл":
                    grade = "MIDDLE"
                if grade == "Сеньор":
                    grade = "SENIOR"
                if grade == "N/A":
                    grade = "NULL"
                day, month, year = people["Дата рождения"].split(".")
                date_birthday = str(year) + "-" + str(month) + "-" + str(day)
                specialization = people["Должность"]
                fact1 = people["Факт 1"]
                fact2 = people["Факт 2"]
                fact3 = people["Факт 3"]
                user_json = {
                    "email": "test" + str(i) + "@test.com",
                    "last_name": last_name,
                    "first_name": first_name,
                    "patronymic": patronymic,
                    "grade": grade,
                    "date_birthday": date_birthday,
                    "specialization": specialization,
                    "fact1": fact1,
                    "fact2": fact2,
                    "fact3": fact3,
                    "password": "pbkdf2_sha256$320000$mg8W8jhiNagFAQ0bUdVhpT$7/D56fxBGnLDyWzhe6WVzRFXCOAbom8q+6hP6oRJ0+4="
                }
                User.objects.create(**user_json)
        return Response("ok", status=status.HTTP_200_OK)


class GetListOfUsers(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)


class GetListOfUsersFilter(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        params = request.query_params
        limit_of_set = int(params.get("limit_of_set", 10))
        page = int(params.get("page", 0))
        order = params.get("order", None)
        filter_fields = {}
        exclude_fields = []
        department = params.get("department", None)
        if department:
            filter_fields.update({"department_members": department})
        not_empty = params.get("not_empty", None)
        if not_empty == "true":
            for item in allowed_fileds_to_filter:
                if item != "patronymic":
                    exclude_fields.append(Q(**{item + "__isnull": True}))
                    exclude_fields.append(Q(**{item: ""}))
        for key, value in params.items():
            if key in allowed_fileds_to_filter:
                if isinstance(value, (str, int)):
                    filter_fields.update({key + "__contains": value})
        if order not in allowed_fileds_to_order or not order:
            order = "last_name"
        if order == "random":
            order = "?"
        start = page * limit_of_set
        last = start + limit_of_set
        users = User.objects.filter(**filter_fields).exclude(reduce(or_, exclude_fields)).order_by(order)[start:last]
        serializer = UserSerializer(users, many=True)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)


class UpdateUserProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        avatar = request.data.get("Avatar")
        serializer_data = request.data
        if avatar:
            serializer_data.update({"avatar": avatar})
        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)


class IntroduceView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_username = request.data.get("user_id")
        is_introduced = request.data.get("status")
        user_filter = User.objects.filter(username=user_username).filter()
        if user_filter:
            user_id = user_filter.first()
            result = UserRelationship.introduce(
                user1=request.user, user2=user_id, introduced=is_introduced
            )
            if result:
                return Response(status=status.HTTP_200_OK)
            return Response({"message": "Already introduced"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "User does not  exist"}, status=status.HTTP_404_NOT_FOUND)


class ObtainToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            login = request.data['login']
            password = request.data['password']
            try:
                user = User.objects.get(email=login)
            except User.DoesNotExist:
                return Response({"error": 'Please provide right login and a password'},
                                status=status.HTTP_401_UNAUTHORIZED)
            if not user.check_password(password) or not user.is_active:
                return Response({"error": 'Please provide right login and a password'},
                                status=status.HTTP_401_UNAUTHORIZED)
            if user:
                try:
                    response = UserSerializer(user, context={"is_auth": True}).data
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
                    return Response(response, status=status.HTTP_200_OK)

                except Exception as e:
                    raise e
        except (KeyError, ObjectDoesNotExist):
            return Response({"error": 'Please provide right login and a password'}, status=status.HTTP_401_UNAUTHORIZED)


class RandomUser(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        requester = request.user
        params = request.query_params
        limit_of_set = int(params.get("limit_of_set", 10))
        uuid_to_exclude = params.get("uuid_to_exclude", "").split(",")
        uuid_to_exclude = list(User.objects.filter(username__in=uuid_to_exclude).values_list("id", flat=True))
        introduced = UserRelationship.objects.filter(user1=requester)
        introduced_values_list = list(introduced.values_list("user2_id", flat=True))
        not_introduced = User.objects.exclude(pk__in=introduced_values_list +[requester.id] + uuid_to_exclude).order_by("?")
        if not_introduced:
            result_user = not_introduced[:limit_of_set]
        else:
            introduced.filter(introduced=False).delete()
            introduced = list(UserRelationship.objects.filter(user1=requester).values_list("user2_id", flat=True))
            not_introduced = User.objects.exclude(pk__in=introduced + [requester.id] + uuid_to_exclude).order_by("?")
            if not_introduced:
                result_user = not_introduced[:limit_of_set]
            else:
                return Response({"message": "You're already introduced to everyone"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(instance=result_user, many=True)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)
