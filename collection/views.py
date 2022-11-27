from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from collection.serializer import (
    PlayCardSerializer,
    PlayCardViewSerializer,
    DepartmentCollectionSerializer,
    UserDepartmentCollectionSerializer,
    CardTradeSerializer,
    CardTradeViewSerializer,
)
from collection.models import PlayCard, CardTrade
from department.models import Department
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


class SpawnPlayCard(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        requester = request.user
        person = (
            User.objects.filter(
                avatar__isnull=False,
                first_name__isnull=False,
                last_name__isnull=False,
                fact1__isnull=False,
            )
            .order_by("?")
            .first()
        )
        data = {"owner": requester.id, "person": person.id}
        serializer = PlayCardSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        result_data = {"owner": requester, "person": person}
        departments = Department.objects.all()
        for department in departments:
            playcard_set = set(
                PlayCard.objects.filter(
                    person__department_members=department, owner=requester
                ).values_list("person_id", flat=True)
            )
            department_members = set(department.members.values_list("id", flat=True))
            if playcard_set == department_members:
                if department.id not in requester.collected_departments:
                    requester.collected_departments.append(department.id)
                    requester.save()
        response = PlayCardViewSerializer(instance=result_data)
        return Response(response.data, status=status.HTTP_201_CREATED)


class PlayCardsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        requester = request.user
        params = request.query_params
        department_id = params.get("department_id")
        user_cards = PlayCard.objects.filter(owner=requester)
        if department_id:
            user_cards = user_cards.filter(
                person__department_members=int(department_id)
            )
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
                user_cards = user_cards.filter(
                    person__department_members=int(department_id)
                )
            serializer = PlayCardViewSerializer(instance=user_cards, many=True)
            response = serializer.data
        except ObjectDoesNotExist:
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_200_OK
            )
        return Response(response, status=status.HTTP_200_OK)


class DepartmentPlayCardView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = DepartmentCollectionSerializer(
            instance=Department.objects.all(), many=True, context={"user": user}
        )
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)


class UserDepartmentPlayCardView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        try:
            user = User.objects.get(username=user_id)
            serializer = UserDepartmentCollectionSerializer(
                instance=Department.objects.all(), many=True, context={"user": user}
            )
            response = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_200_OK
            )


class PointsForDepartment(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        department_id = request.data.get("department_id", None)
        try:
            department = Department.objects.get(id=department_id)
            playcard_set = set(
                PlayCard.objects.filter(
                    person__department_members=department, owner=user
                ).values_list("person_id", flat=True)
            )
            department_members = set(department.members.values_list("id", flat=True))
            if playcard_set == department_members:
                if department.id not in user.collected_departments:
                    user.collected_departments.append(department.id)
                    user.save()
                    return Response(
                        {"message": "Points received"}, status=status.HTTP_200_OK
                    )
                return Response(
                    {"message": "You already received "},
                    status=status.HTTP_403_FORBIDDEN,
                )
            return Response(
                {"message": "You don't have full department"},
                status=status.HTTP_403_FORBIDDEN,
            )
        except ObjectDoesNotExist:
            return Response(
                {"message": "Department does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class RequestTrade(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user1 = request.user
        user2 = request.data.get("user2")
        user2 = User.objects.filter(username=user2)
        offered_cards = request.data.get("offered_cards")
        requested_cards = request.data.get("requested_cards")
        if user2:
            user2 = user2.first()
        else:
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        offered_cards = PlayCard.objects.filter(id__in=offered_cards, owner=user1)
        offered_cards_list = list(offered_cards.values_list("id", flat=True))
        requested_cards = PlayCard.objects.filter(id__in=requested_cards, owner=user2)
        requested_cards_list = list(requested_cards.values_list("id", flat=True))
        data = {
            "user1": user1.id,
            "user2": user2.id,
            "user1_cards": offered_cards_list,
            "user2_cards": requested_cards_list,
        }
        serializer = CardTradeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        result_data = {
            "user1": user1,
            "user2": user2,
            "user1_cards": offered_cards,
            "user2_cards": requested_cards,
            "id": serializer.data.get("id"),
        }
        response = CardTradeViewSerializer(instance=result_data)
        return Response(response.data, status=status.HTTP_201_CREATED)


class TradeOffers(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        trades = CardTrade.objects.filter(user2=user)
        result_lust = []
        for trade in trades:
            data = {
                "id": trade.id,
                "user1": user,
                "user2": trade.user2,
                "user1_cards": PlayCard.objects.filter(id__in=trade.user1_cards),
                "user2_cards": PlayCard.objects.filter(id__in=trade.user2_cards),
            }
            result_lust.append(data)
        return Response(
            CardTradeViewSerializer(instance=result_lust, many=True).data,
            status=status.HTTP_200_OK,
        )


class TradeRequests(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        trades = CardTrade.objects.filter(user1=user)
        result_lust = []
        for trade in trades:
            data = {
                "id": trade.id,
                "user1": user,
                "user2": trade.user2,
                "user1_cards": PlayCard.objects.filter(id__in=trade.user1_cards),
                "user2_cards": PlayCard.objects.filter(id__in=trade.user2_cards),
            }
            result_lust.append(data)
        return Response(
            CardTradeViewSerializer(instance=result_lust, many=True).data,
            status=status.HTTP_200_OK,
        )


class AcceptTrade(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        trade_id = request.data.get("trade_id")
        accept = request.data.get("accept")
        if trade := CardTrade.objects.filter(user2=user, pk=trade_id):
            trade = trade.first()
            if accept:
                PlayCard.objects.filter(pk__in=trade.user1_cards).update(
                    **{"owner": trade.user2}
                )
                PlayCard.objects.filter(pk__in=trade.user2_cards).update(
                    **{"owner": trade.user1}
                )
                trade.delete()
                return Response(
                    {"message": "Successful trade"}, status=status.HTTP_200_OK
                )
            trade.delete()
            return Response({"message": "Trade rejected"}, status=status.HTTP_200_OK)
        return Response({"message": "No rights"}, status=status.HTTP_403_FORBIDDEN)
