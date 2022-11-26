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
            if product_to_update:
                del data["id"]
                product_to_update.update(**data)
                product = Products.objects.get(pk=product_id)
                serializer = ProductsSerializer(instance=product)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ProductsSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)


class DeleteProduct(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        data = request.data
        product_id = data.get("id")
        Products.objects.filter(id=product_id).delete()
        return Response(status=status.HTTP_200_OK)


class GetProduct(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        params = request.query_params
        product_id = params.get("id")
        try:
            data = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductsSerializer(instance=data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetProductList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        params = request.query_params
        page = int(params.get("page", 0))
        limit_of_set = int(params.get("limit_of_set", 10))
        start = page * limit_of_set
        last = start + limit_of_set
        data = Products.objects.all()[start:last]
        serializer = ProductsSerializer(instance=data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
