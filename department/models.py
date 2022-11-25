from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Department(models.Model):
    title = models.CharField(max_length=100)
    chief = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, null=True, blank=True)
    head_department = models.ForeignKey(to="self", on_delete=models.DO_NOTHING, null=True, blank=True)
    members = models.ManyToManyField(to=User, blank=True, related_name="department_members")


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")
        db_table = "department"
