from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class PlayCard(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False, null=False, related_name="collection_owner")
    person = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False, null=False, related_name="collection_person")

