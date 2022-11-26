from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from collection.serializer import PlayCardSerializer, PlayCardViewSerializer
from collection.models import PlayCard
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
User = get_user_model()


class SpawnPlayCard(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        requester = request.user
        person = User.objects.order_by("?").first()
        data = {"owner": requester.id, "person": person.id}
        serializer = PlayCardSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Playcard successfully created"}, status=status.HTTP_201_CREATED)


class PlayCardsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        requester = request.user
        user_cards = PlayCard.objects.filter(owner=requester)
        serializer = PlayCardViewSerializer(instance=user_cards, many=True)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)


class UserPlayCardsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        try:
            user = User.objects.get(username=user_id)
            user_cards = PlayCard.objects.filter(owner=user)
            serializer = PlayCardViewSerializer(instance=user_cards, many=True)
            response = serializer.data
        except ObjectDoesNotExist:
            return Response({"message": "User does not exist"}, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_200_OK)


class DepartmentPlayCardView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, user_id):
        try:
            user = User.objects.get(username=user_id)
            user_cards = PlayCard.objects.filter(owner=user)
            serializer = PlayCardViewSerializer(instance=user_cards, many=True)
            response = serializer.data
        except ObjectDoesNotExist:
            return Response({"message": "User does not exist"}, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_200_OK)

