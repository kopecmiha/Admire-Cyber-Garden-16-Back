from django.db.models import Sum
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.utils import get_user_balance
from statistic.models import GameSession
from statistic.serializer import GameSessionSerializer


class ReplenishmentGameSession(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        serializer = GameSessionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = serializer.data
        GameSession.objects.filter(pk=int(response["id"])).update(user=request.user)
        return Response(response, status=status.HTTP_200_OK)


class GetUserBalance(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        balance = get_user_balance(request.user)
        return Response({"balance": balance}, status=status.HTTP_200_OK)
