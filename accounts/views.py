import json
import random
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
from department.models import Department

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
    "city",
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
        stajeri_department = Department.objects.filter(title="Стажеры")
        if stajeri_department:
            stajeri_department = stajeri_department.first()
            stajeri_department.members.add(user)
            stajeri_department.save()
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
        user = request.user
        params = request.query_params
        limit_of_set = int(params.get("limit_of_set", 10))
        page = int(params.get("page", 0))
        order = params.get("order", None)
        introduced = params.get("introduced", False)
        not_introduced = params.get("not_introduced", False)
        filter_fields = {}
        exclude_fields = [Q(**{"id__isnull": True})]
        department = params.get("department", None)
        if department:
            filter_fields.update({"department_members": department})
        not_empty = params.get("not_empty", None)
        if not_empty:
            not_empty_fields = not_empty.split(",")
            for item in not_empty_fields:
                if item in allowed_fileds_to_filter or item == "avatar":
                    exclude_fields.append(Q(**{item + "__isnull": True}))
                    exclude_fields.append(Q(**{item: ""}))
                elif item == "department":
                    exclude_fields.append(Q(**{"department_members": None}))
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
        users = User.objects.filter(**filter_fields).exclude(reduce(or_, exclude_fields))
        if introduced:
            introduced = UserRelationship.objects.filter(user1=user)
            introduced_values_list = list(introduced.values_list("user2_id", flat=True))
            users = users.filter(pk__in=introduced_values_list)
        if not_introduced:
            introduced = UserRelationship.objects.filter(user1=user)
            introduced_values_list = list(introduced.values_list("user2_id", flat=True))
            users = users.exclude(pk__in=introduced_values_list)
        users = users.order_by(order)[start:last]
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
        not_introduced = User.objects.exclude(
            pk__in=introduced_values_list + [requester.id] + uuid_to_exclude).order_by("?")
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


class ChangePassword(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            return Response({"error": "Empty password"}, status=status.HTTP_403_FORBIDDEN)
        if user.check_password(old_password):
            user.password = make_password(new_password)
            user.save()
        else:
            return Response({"error": "Not valid password"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"message": "Successfully change password"}, status=status.HTTP_200_OK)


class IsIntroduced(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        params = request.query_params
        user1 = params.get("user1")
        user2 = params.get("user2")
        user1 = User.objects.get(username=user1)
        user2 = User.objects.get(username=user2)
        if UserRelationship.objects.filter(user1=user1, user2=user2).exists():
            return Response({"is_introduced": True}, status=status.HTTP_200_OK)
        return Response({"is_introduced": False}, status=status.HTTP_204_NO_CONTENT)


class TextSearch(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        params = request.query_params
        search_text = params.get("search_text")
        page = int(params.get("page", 0))
        limit_of_set = int(params.get("limit_of_set", 10))
        start = page * limit_of_set
        last = start + limit_of_set
        filter_fields = []
        query_filter = Q(id__gte=0)
        if search_text:
            for item in allowed_fileds_to_filter + ["fact1"]:
                filter_fields.append(Q(**{item + "__icontains": search_text}))
                query_filter = reduce(or_, filter_fields)
        search_results = User.objects.filter(query_filter)[start:last]
        result = UserSerializer(instance=search_results, many=True)
        return Response(result.data, status=status.HTTP_204_NO_CONTENT)


class RelatedCount(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_count = User.objects.all().count()
        introduced_count = UserRelationship.objects.filter(Q(user1=request.user) & Q(introduced=True)).count()
        return Response({"all_count": all_count, "introduced_count": introduced_count}, status=status.HTTP_200_OK)
