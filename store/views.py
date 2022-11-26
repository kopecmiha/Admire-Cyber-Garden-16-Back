from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from store.models import Products
from store.serializer import ProductsSerializer


class ReplenishmentProduct(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        product_id = data.get("id")
        if product_id:
            product_to_update = Products.objects.filter(id=product_id)
            print(product_to_update)
        else:
            serializer = ProductsSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)
