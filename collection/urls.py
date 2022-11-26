from django.urls import path
from .views import SpawnPlayCard, PlayCardsView, UserPlayCardsView

urlpatterns = [
    path('spawn_playcard/', SpawnPlayCard.as_view()),
    path('play_cards/', PlayCardsView.as_view()),
    path('user_play_cards/<str:user_id>/', UserPlayCardsView.as_view()),
   # path('get_department/<int:department_id>', GetDepartment.as_view()),
   # path('add_to_department/', AddToDepartment.as_view()),

]