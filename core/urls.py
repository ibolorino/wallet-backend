from django.urls import path
from .views import *


urlpatterns = [
    # path('', signatures_list, name='signatures_list'),
    # path('<int:id>', detalhe_assinatura, name='detalhe_assinatura'),
    path('stocks', StockList.as_view()),
    path('orders', orders),
    path('orders/detail/<int:pk>', detail_order),
    path('wallets', wallets),
    path('wallets/detail/<int:pk>', detail_wallet),
]