from django.db import models
from django.core.validators import MinValueValidator
from .validators import value_validator, tax_validator

class Order(models.Model):
    type_choices = (
        ('B', 'Buy'),
        ('S', 'Sell'),
    )
    stock = models.ForeignKey("Stock", on_delete=models.PROTECT)
    quantity = models.IntegerField("Quantity", validators=[MinValueValidator(1)])
    type_order = models.CharField("Type", max_length=1, choices=type_choices)
    value = models.DecimalField("Value", max_digits=13, decimal_places=2, validators=[value_validator])
    tax = models.DecimalField("Tax", max_digits=5, decimal_places=2, validators=[tax_validator])
    date = models.DateField("Date", auto_now_add=True)
    person = models.ForeignKey("person.Person", on_delete=models.CASCADE)

    def __str__(self):
        return self.stock.ticker + " - " + str(self.date)

    def orders_by_person(self, person):
        orders = Order.objects.filter(person=person)
        return orders


class Stock(models.Model):
    company_name = models.CharField("Company Name", max_length=255)
    ticker = models.CharField("Ticker", max_length=10, unique=True)
    current_value = models.DecimalField("Current Value", max_digits=6, decimal_places=2)

    def __str__(self):
        return self.ticker

    def get_stock_by_ticker(self, ticker):
        if len(Stock.objects.filter(ticker=ticker)) > 0:
            return Stock.objects.filter(ticker=ticker)[0]  
        else:
            return None


class Wallet(models.Model):
    stock = models.ForeignKey("Stock", on_delete=models.PROTECT)
    person = models.ForeignKey("person.Person", on_delete=models.CASCADE)
    quantity = models.IntegerField("Quantity", validators=[MinValueValidator(1)])
    average_price = models.DecimalField("Average Price", max_digits=6, decimal_places=2, null=True)
    total_value = models.DecimalField("Total Value", max_digits=15, decimal_places=2)

    def __str__(self):
        return self.person.name + " - " + self.stock.ticker

    def wallets_by_person(self, person):
        wallets = Wallet.objects.filter(person=person)
        return wallets

    def update_wallet(self, order, person):
        try:
            current_wallet = Wallet.objects.get(stock__ticker=order.stock.ticker)
        except:
            current_wallet = Wallet()
        quantity = int(current_wallet.quantity or 0)
        average_price = float(current_wallet.average_price or 0.0)
        total_value = float(current_wallet.total_value or 0.0)
        if order.type_order == 'B':
            total_value = total_value + float(order.value) + float(order.tax)
            quantity += order.quantity
            average_price = total_value / quantity
        else:
            quantity -= order.quantity
            total_value = total_value - float(order.value) + float(order.tax)
            if quantity == 0:
                average_price = 0
            else:
                average_price = total_value / quantity
        if current_wallet.pk is not None:
            current_wallet = Wallet.objects.filter(pk=current_wallet.pk).update(quantity=quantity, average_price=average_price, total_value=total_value)
        else:
            current_wallet = Wallet.objects.create(stock=order.stock, person=person, quantity=quantity, average_price=average_price, total_value=total_value)
        return current_wallet

    def get_quantity(self, stock, person):
        try:
            wallet = Wallet.objects.get(stock=stock, person=person)
            return wallet.quantity
        except:
            return 0