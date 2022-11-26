from django.db import models
from django.utils import timezone

from accounts.models import User


class GameSession(models.Model):
    class GamesTypeEnum(models.TextChoices):
        full_name = "full-name"
        mapping = "mapping"
        excluding = "excluding"
        swiper = "swiper"

    duration = models.BigIntegerField(default=0)
    finished = models.DateTimeField(default=timezone.now)
    points = models.IntegerField(default=0)
    game_type = models.CharField(
        max_length=10, choices=GamesTypeEnum.choices, null=True
    )
    try_count = models.IntegerField(default=0)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "GameSession"
        verbose_name_plural = "GameSession"
        db_table = "game_sessions"
