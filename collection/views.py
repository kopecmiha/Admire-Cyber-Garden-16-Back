from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from collection.serializer import PlayCardSerializer, PlayCardViewSerializer, DepartmentCollectionSerializer, UserDepartmentCollectionSerializer
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
        response = serializer.data
        return Response(response, status=status.HTTP_201_CREATED)


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
            serializer = UserDepartmentCollectionSerializer(instance=Department.objects.all(), many=True, context={"user": user})
            response = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "User does not exist"}, status=status.HTTP_200_OK)


class PointsForDepartment(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user = request.user
        department_id = request.data.get("department_id", None)
        try:
            department = Department.objects.get(id=department_id)
            playcard_set = set(
            PlayCard.objects.filter(person__department_members=department, owner=user).values_list(
                "person_id", flat=True))
            department_members = set(department.members.values_list("id", flat=True))
            if playcard_set == department_members:
                if department.id not in user.collected_departments:
                    user.collected_departments.append(department.id)
                    user.save()
                    return Response({"message": "Points received"}, status=status.HTTP_200_OK)
                return Response({"message": "You already received "}, status=status.HTTP_403_FORBIDDEN)
            return Response({"message": "You don't have full department"}, status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response({"message": "Department does not exist"}, status=status.HTTP_404_NOT_FOUND)

'''
class RequestTrade(APIView):
    permission_classes = (IsAuthenticated, )
    
    
    def post(self, request):'''