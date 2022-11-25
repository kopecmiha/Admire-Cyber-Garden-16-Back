from django.urls import path
from .views import CreateDepartment, UpdateDepartment, DeleteDepartment, GetDepartments

urlpatterns = [
    path('create_department/', CreateDepartment.as_view()),
    path('update_department/', UpdateDepartment.as_view()),
    path('delete_department/', DeleteDepartment.as_view()),
    path('get_departments/', GetDepartments.as_view()),

]