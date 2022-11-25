import re

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
from accounts.permissions import IsTeacherOrDean, IsDean
from accounts.serializer import UserSerializer, UserProfileSerializer
from main import settings


class CreateUser(APIView):
    permission_classes = (IsTeacherOrDean,)

    def post(self, request):
        request = request.data
        user_status = request["status"]
        if user_status == "DEAN":
            return Response({"error": "You can create dean account only with invite code"},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(data=request)
        serializer.is_valid(raise_exception=True)
        serializer.save(password=make_password(request['password']))
        return Response({"message": "User succesfully created"}, status=status.HTTP_201_CREATED)


class GetUserProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)


class UpdateUserProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        avatar = request.data.get("Avatar")
        serializer_data = request.data
        if avatar:
            serializer_data.update({"avatar": avatar})
        serializer = UserProfileSerializer(
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
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY)
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
                    return Response({'token': token}, status=status.HTTP_200_OK)

                except Exception as e:
                    raise e
        except (KeyError, ObjectDoesNotExist):
            return Response({"error": 'Please provide right login and a password'}, status=status.HTTP_401_UNAUTHORIZED)
