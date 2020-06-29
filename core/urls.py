from django.urls import path
from .views import *


urlpatterns = [
    # path('', signatures_list, name='signatures_list'),
    # path('<int:id>', detalhe_assinatura, name='detalhe_assinatura'),
    path('stocks', StockList.as_view()),
    path('orders', orders),
    path('wallets', wallets)
]