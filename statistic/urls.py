from django.urls import path
from .views import ReplenishmentGameSession, GetUserBalance

urlpatterns = [
    path("add_game_session/", ReplenishmentGameSession.as_view()),
    path("get_user_balance/", GetUserBalance.as_view()),
]
