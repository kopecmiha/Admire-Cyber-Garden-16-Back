from rest_framework import serializers
from .models import Products, TradeStory


class ProductsSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Products
        fields = "id", "title", "icons", "price", "in_stock",
        extra_kwargs = {"id": {'read_only': True}, "icons": {'read_only': True}}


class TradeStorySerializer(serializers.ModelSerializer):
    product = ProductsSerializer()

    class Meta(object):
        model = TradeStory
        fields = "id", "product", "price", "date_time",
