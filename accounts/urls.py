from django.urls import path
from .views import CreateUser, GetUserProfile, ObtainToken, UpdateUserProfile, Parse, GetListOfUsers

urlpatterns = [
    path('create_user/', CreateUser.as_view()),
    path('obtain_token/', ObtainToken.as_view()),
    path('get_profile/', GetUserProfile.as_view()),
    path('update_profile/', UpdateUserProfile.as_view()),
    path('list_of_users/', GetListOfUsers.as_view()),
    path('parse/', Parse.as_view()),
]