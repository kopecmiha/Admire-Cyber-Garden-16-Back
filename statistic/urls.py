from django.urls import path
from .views import ReplenishmentGameSession, GetUserPoints

urlpatterns = [
    path('add_game_session/', ReplenishmentGameSession.as_view()),
    path('get_user_points/', GetUserPoints.as_view()),
]