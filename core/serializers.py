from rest_framework import serializers
from .models import *

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    #stock = StockSerializer(many = False)

    class Meta:
        model = Order
        fields = ('id', 'stock', 'quantity', 'type_order', 'value', 'tax', 'date', 'person')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['stock'] = StockSerializer(instance.stock).data
        return response

    def validate(self, data):
        if data['type_order'] == 'S':
            person = data['person'].id
            stock = data['stock'].id
            initial_quantity = Wallet().get_quantity(stock, person)
            if data['quantity'] > initial_quantity:
                raise serializers.ValidationError("You can't sell more than you have.")
        return data


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ('id', 'stock', 'quantity', 'average_price', 'person', 'total_value')
        extra_kwargs = {'average_price': {'read_only': True}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['stock'] = StockSerializer(instance.stock).data
        return response

    def validate(self, data):
        data['average_price'] = data['total_value'] / data['quantity']
        return data