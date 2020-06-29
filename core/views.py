from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
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
    queryset = Stock.objects.all()
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
        quantity = data['quantity']
        type_order = data['type_order']
        value = data['value']
        tax = data['tax']
        date = data['date']
        #TODO: need to validate input values
        person = request.user.person
        # validate_order(stock, quantity, type_order, value, tax, date, person)
        new_order = Order().new_order(stock=stock, quantity=quantity, type_order=type_order, value=value, tax=tax, person=person)
        serializer = OrderSerializer(new_order)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def wallets(request):
    if request.method == 'GET':
        person = request.user.person
        wallets = Wallet().wallets_by_person(person)
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        pass
