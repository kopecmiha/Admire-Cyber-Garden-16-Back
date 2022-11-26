from django.urls import path
from .views import ReplenishmentProduct, DeleteProduct, GetProduct, GetProductList, Buy, TradingHistory

urlpatterns = [
    path('replenishment_product/', ReplenishmentProduct.as_view()),
    path('delete_product/', DeleteProduct.as_view()),
    path('get_product/', GetProduct.as_view()),
    path('get_products_list/', GetProductList.as_view()),
    path('buy/', Buy.as_view()),
    path('trading_history/', TradingHistory.as_view()),
]