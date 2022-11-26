from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from collection.serializer import PlayCardSerializer, PlayCardViewSerializer, DepartmentCollectionSerializer
from collection.models import PlayCard
from department.models import Department
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
        params = request.query_params
        department_id = params.get("department_id")
        user_cards = PlayCard.objects.filter(owner=requester)
        if department_id:
            user_cards = user_cards.filter(person__department_members=int(department_id))
        serializer = PlayCardViewSerializer(instance=user_cards, many=True)
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)


class UserPlayCardsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        try:
            params = request.query_params
            department_id = params.get("department_id")
            user = User.objects.get(username=user_id)
            user_cards = PlayCard.objects.filter(owner=user)
            if department_id:
                user_cards = user_cards.filter(person__department_members=int(department_id))
            serializer = PlayCardViewSerializer(instance=user_cards, many=True)
            response = serializer.data
        except ObjectDoesNotExist:
            return Response({"message": "User does not exist"}, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_200_OK)


class DepartmentPlayCardView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        serializer = DepartmentCollectionSerializer(instance=Department.objects.all(), many=True, context={"user": user})
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)


class UserDepartmentPlayCardView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, user_id):
        try:
            user = User.objects.get(username=user_id)
            serializer = DepartmentCollectionSerializer(instance=Department.objects.all(), many=True, context={"user": user})
            response = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "User does not exist"}, status=status.HTTP_200_OK)

