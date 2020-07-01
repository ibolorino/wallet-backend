from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from .models import *
from person.models import Person
from .serializers import *
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)


class StockList(generics.ListCreateAPIView):
    queryset = Stock.objects.all().order_by('ticker', 'company_name')
    serializer_class = StockSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def orders(request):
    print(request.method)
    if request.method == 'GET':
        person = request.user.person
        orders = Order().orders_by_person(person)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        stock = Stock().get_stock_by_ticker(data['stock'])
        person = request.user.person
        data['person'] = person.id
        data['stock'] = 0
        if stock:
            data['stock'] = stock.id
        serializer = OrderSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            order = Order.objects.get(pk=serializer.data['id'])
            Wallet().update_wallet(order, person)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def wallets(request):
    if request.method == 'GET':
        person = request.user.person
        wallets = Wallet().wallets_by_person(person)
        wallets = wallets.filter(quantity__gt=0)
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        pass
