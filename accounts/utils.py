from django.db.models import Sum, IntegerField, Count
from django.db.models.functions import Coalesce
from rest_framework_jwt.serializers import jwt_payload_handler
import jwt

from department.models import Department
from main import settings
from statistic.models import GameSession
from store.models import TradeStory


def get_jwt_token(user):
    payload = jwt_payload_handler(user)
    token = jwt.encode(payload, settings.SECRET_KEY)
    return token

def get_user_balance(user):
    collection_income = Department.objects.filter(
        id__in=user.collected_departments).annotate(members_count=Count('members')).values_list("members_count", flat=True)
    collection_income = sum(list(collection_income)) * 10
    income = GameSession.objects.filter(user=user).aggregate(points_sum=Sum('points'))
    income = income.get("points_sum") if income.get("points_sum") else 0
    expences = TradeStory.objects.filter(user=user).aggregate(points_sum=Sum('price'))
    expences = expences.get("points_sum") if expences.get("points_sum") else 0
    balance = collection_income + income - expences
    return balance