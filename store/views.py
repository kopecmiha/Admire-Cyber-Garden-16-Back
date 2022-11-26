from django.db.models import Q
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from accounts.utils import get_user_balance
from store.models import Products, TradeStory
from store.serializer import ProductsSerializer, TradeStorySerializer


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


class Buy(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        product_id = data.get("id")
        balance = get_user_balance(request.user)
        product = Products.objects.filter(Q(id=product_id) & Q(price__lte=balance))
        if product:
            product = product.first()
            new_buy = TradeStory.objects.create(user=request.user, product=product, price=product.price)
            response = TradeStorySerializer(instance=new_buy).data
        else:
            return Response({"error": "You can't buy this product"}, status=status.HTTP_403_FORBIDDEN)
        return Response(response, status=status.HTTP_200_OK)


class TradingHistory(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        history = TradeStory.objects.filter(user=request.user)
        response = TradeStorySerializer(instance=history, many=True).data
        return Response(response, status=status.HTTP_200_OK)
