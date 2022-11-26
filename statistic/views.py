from django.db.models import Sum
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
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


class GetUserPoints(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.query_params.get("user_uuid", None)
        if user_id:
            user_filter = {"user__username": user_id}
        else:
            user_filter = {"user": request.user}
        score = GameSession.objects.filter(**user_filter).aggregate(points_sum=Sum('points'))
        return Response(score, status=status.HTTP_200_OK)
