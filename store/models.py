from django.db import models
from django.utils import timezone

from accounts.models import User


class Products(models.Model):
    title = models.CharField(max_length=100, default="")
    icons = models.FileField(upload_to="icons", null=True, blank=True)
    price = models.IntegerField(null=False, default=0)
    in_stock = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Products"
        verbose_name_plural = "Products"
        db_table = "products"


class TradeStory(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(to=Products, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.IntegerField(null=False, default=0)
    date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "TradeStory"
        verbose_name_plural = "TradeStory"
        db_table = "trade_story"
