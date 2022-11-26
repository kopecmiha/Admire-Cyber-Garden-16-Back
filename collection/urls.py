from django.urls import path
from .views import SpawnPlayCard, PlayCardsView, UserPlayCardsView, DepartmentPlayCardView, UserDepartmentPlayCardView, PointsForDepartment, RequestTrade

urlpatterns = [
    path('spawn_playcard/', SpawnPlayCard.as_view()),
    path('play_cards/', PlayCardsView.as_view()),
    path('user_play_cards/<str:user_id>/', UserPlayCardsView.as_view()),
    path('play_card_departments/', DepartmentPlayCardView.as_view()),
    path('user_play_card_departments/<str:user_id>/', UserDepartmentPlayCardView.as_view()),
    path('points_for_department/', PointsForDepartment.as_view()),
    path('request_trade/', RequestTrade.as_view()),
]