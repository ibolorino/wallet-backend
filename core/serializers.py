from rest_framework import serializers
from .models import *

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    stock = StockSerializer(many = False, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'stock', 'quantity', 'type_order', 'value', 'tax', 'date', 'person')


class WalletSerializer(serializers.ModelSerializer):
    stock = StockSerializer(many = False, read_only=True)

    class Meta:
        model = Wallet
        fields = ('stock', 'quantity', 'average_price', 'person')