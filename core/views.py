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
    if request.method == 'GET':
        person = request.user.person
        orders = Order().orders_by_person(person).order_by('date')
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
            Wallet().update_wallet_on_order(order, person)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def detail_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    person = request.user.person
    if request.method == 'DELETE':
        Wallet().update_wallet_on_delete_order(order, person)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def wallets(request):
    if request.method == 'GET':
        person = request.user.person
        wallets = Wallet().wallets_by_person(person).filter(quantity__gt=0).order_by('stock__ticker')
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        stock = Stock().get_stock_by_ticker(data['stock'])
        person = request.user.person
        data['person'] = person.id
        data['stock'] = 0
        person_wallet = Wallet().wallets_by_person(person).filter(stock__id=stock.id)
        if stock:
            data['stock'] = stock.id
        serializer = WalletSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            data['average_price'] = serializer.validated_data['average_price']
            if len(person_wallet) == 0:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                wallet = Wallet().add_wallet(person_wallet, data)
                print(wallet.values()[0])
                return Response(wallet.values()[0], status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
