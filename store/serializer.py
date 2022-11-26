from rest_framework import serializers
from .models import Products
from department.models import Department


class ProductsSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Products
        fields = "id", "title", "icons", "price", "in_stock",
        extra_kwargs = {"id": {'read_only': True}, "icons": {'read_only': True}}
