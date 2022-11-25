from django.contrib import admin

from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    User
    """

    list_display = "id", "email", "first_name", "last_name"
    list_display_links = "id", "email", "first_name", "last_name"
    search_fields = "id",
