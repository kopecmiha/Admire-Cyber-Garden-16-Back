import re
import uuid

import jwt
from django.contrib.auth import user_logged_in
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import jwt_payload_handler

from accounts.models import User
from accounts.serializer import UserSerializer, UserCreateSerializer, UserAuthSerializer
from accounts.utils import get_jwt_token
from main import settings


class CreateUser(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        request = request.data
        request["username"] = uuid.uuid4()
        serializer = UserCreateSerializer(data=request)
        serializer.is_valid(raise_exception=True)
        serializer.save(password=make_password(request['password']))
        #user = User.objects.get(email=serializer.data["email"])
        #token = get_jwt_token(user)
        #user_data = {"token": token, user: user}
        #response = UserAuthSerializer
        #user_logged_in.send(sender=user.__class__,
        #                    request=request, user=user)
        return Response("aaaa", status=status.HTTP_201_CREATED)


class GetUserProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
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
                    token = get_jwt_token(user)
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
                    return Response({'token': token}, status=status.HTTP_200_OK)

                except Exception as e:
                    raise e
        except (KeyError, ObjectDoesNotExist):
            return Response({"error": 'Please provide right login and a password'}, status=status.HTTP_401_UNAUTHORIZED)
