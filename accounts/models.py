from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.contrib.postgres.fields import ArrayField


class User(AbstractBaseUser, PermissionsMixin):
    class GradeEnum(models.TextChoices):
        SENIOR = "SENIOR"
        MIDDLE = "MIDDLE"
        JUNIOR = "JUNIOR"
        NULL = "NULL"
    username = models.CharField(_("Username"), default=uuid4, editable=False, unique=True, max_length=100)
    email = models.EmailField(_("Email address"), unique=True, null=True, blank=False)
    first_name = models.CharField(_("First name"), max_length=30, null=True, blank=True)
    last_name = models.CharField(_("Last name"), max_length=30, null=True, blank=True)
    patronymic = models.CharField(_("Patronymic"), max_length=30, null=True, blank=True)
    is_active = models.BooleanField(_("Active"), default=True)
    is_staff = models.BooleanField(_("Is staff"), default=False)
    is_superuser = models.BooleanField(_("Is superuser"), default=False)
    avatar = models.FileField(_("Avatar"), upload_to="avatars", null=True, blank=True)
    grade = models.CharField(
        _("Grade"),
        max_length=10,
        choices=GradeEnum.choices,
        default=GradeEnum.JUNIOR,
    )
    specialization = models.CharField(_("Specialization"), max_length=256, null=True, blank=True)
    date_birthday = models.DateField(null=True, blank=True)
    fact1 = models.TextField(null=True, blank=True)
    fact2 = models.TextField(null=True, blank=True)
    fact3 = models.TextField(null=True, blank=True)
    collected_departments = ArrayField(models.IntegerField(), default=list)
    city = models.CharField(_("City"), max_length=30, null=True, blank=True)
    online = models.BooleanField(_("Online"), null=True, default=False)
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("User")
        db_table = "auth_user"


class UserRelationship(models.Model):
    user1 = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False, null=False, related_name="relationship1")
    user2 = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False, null=False, related_name="relationship2")
    introduced = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        verbose_name = _("UserRelationship")
        verbose_name_plural = _("UserRelationships")
        db_table = "user_relationship"
        unique_together = ("user1", "user2",)

    @staticmethod
    def introduce(user1, user2, introduced):
        try:
            relationship = UserRelationship.objects.create(user1=user1, user2=user2, introduced=introduced)
            relationship.save()
            return True
        except Exception as e:
            return False
