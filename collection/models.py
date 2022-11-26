from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import ArrayField

User = get_user_model()


class PlayCard(models.Model):
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="collection_owner",
    )
    person = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="collection_person",
    )


class CardTrade(models.Model):
    user1 = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="trade_user1",
    )
    user2 = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="trade_user2",
    )
    user1_cards = ArrayField(models.IntegerField(), default=list, null=True, blank=True)
    user2_cards = ArrayField(models.IntegerField(), default=list, null=True, blank=True)
