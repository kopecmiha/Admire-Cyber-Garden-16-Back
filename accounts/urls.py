from django.urls import path
from .views import CreateUser, GetUserProfile, ObtainToken, UpdateUserProfile, GetListOfUsers, \
    GetListOfUsersFilter, UserProfile, IntroduceView, RandomUser, IsIntroduced, ChangePassword, TextSearch, RelatedCount

urlpatterns = [
    path('create_user/', CreateUser.as_view()),
    path('obtain_token/', ObtainToken.as_view()),
    path('get_profile/', GetUserProfile.as_view()),
    path('user_profile/<str:id>/', UserProfile.as_view()),
    path('update_profile/', UpdateUserProfile.as_view()),
    path('list_of_users/', GetListOfUsers.as_view()),
    path('list_of_users_filter/', GetListOfUsersFilter.as_view()),
    path('introduce_users/', IntroduceView.as_view()),
    path('is_introduced/', IsIntroduced.as_view()),
    path('random_user/', RandomUser.as_view()),
    path('change_password/', ChangePassword.as_view()),
    path('text_search/', TextSearch.as_view()),
    path('related_count/', RelatedCount.as_view()),
]