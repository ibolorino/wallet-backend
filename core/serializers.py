from rest_framework import serializers
from .models import *

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"

    # def validate(self, data):
    #     """
    #         Recebe um dicionario com os dados do serializer e valida. Útil para validações que comparam mais de um campo.
    #     """
    #     if data['ticker'] != "BLRS3":
    #         raise serializers.ValidationError("Ticker de novo!")
    #     return data

    # def validate_ticker(self, value):
    #   """
    #       Faz a validação de apenas um campo, passado através do parâmetro 'value'
    #   """
    #     if value != "BLRS3":
    #         raise serializers.ValidationError("Ticker não é BLRS3")
    #     return value


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
    stock = StockSerializer(many = False, read_only=True)

    class Meta:
        model = Wallet
        fields = ('id', 'stock', 'quantity', 'average_price', 'person')