
from django.utils.translation import gettext_lazy as _
from accounts.models import User

from django.db import models


class Department(models.Model):
    title = models.CharField(max_length=100)
    chief = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, null=True, blank=True)
    head_department = models.ForeignKey(to="self", on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")
        db_table = "department"
