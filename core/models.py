from django.db import models
from django.core.validators import MinValueValidator

class Order(models.Model):
    type_choices = (
        ('B', 'Buy'),
        ('S', 'Sell'),
    )
    stock = models.ForeignKey("Stock", on_delete=models.PROTECT)
    quantity = models.IntegerField("Quantity", validators=[MinValueValidator(1)])
    type_order = models.CharField("Type", max_length=1, choices=type_choices)
    value = models.DecimalField("Value", max_digits=13, decimal_places=2)
    tax = models.DecimalField("Tax", max_digits=5, decimal_places=2)
    date = models.DateField("Date", auto_now_add=True)
    person = models.ForeignKey("person.Person", on_delete=models.CASCADE)

    def __str__(self):
        return self.stock.ticker + " - " + str(self.date)

    def new_order(self, **kwargs):
        stock = kwargs.get('stock')
        quantity = kwargs.get('quantity')
        type_order = kwargs.get('type_order')
        value = kwargs.get('value')
        tax = kwargs.get('tax')
        person = kwargs.get('person')
        init_quantity = Wallet().get_quantity(stock, person)
        if (quantity > init_quantity) and (type_order == 'S'):
            return "Invalid order. You have {} {} stocks and can't sell {} stocks.".format(init_quantity, stock.ticker, quantity)
        new_order = Order.objects.create(stock=stock, quantity=quantity, type_order=type_order, value=value, tax=tax, person=person)
        Wallet().update_wallet(new_order, person)
        return new_order

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
    average_price = models.DecimalField("Average Price", max_digits=6, decimal_places=2)

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
        average_price = int(current_wallet.average_price or 0)
        total_value = quantity * average_price
        if order.type_order == 'B':
            total_value += order.value + order.tax
            quantity += order.quantity
            average_price = total_value / quantity
        else:
            if order.quantity > quantity:
                return "It's not possible to sell more than you have."
            else:
                quantity -= order.quantity
                total_value += -order.value + order.tax
                if quantity == 0:
                    average_price = 0
                else:
                    average_price = total_value / quantity
        if current_wallet.pk is not None:
            current_wallet = Wallet.objects.filter(pk=current_wallet.pk).update(quantity=quantity, average_price=average_price)
        else:
            current_wallet = Wallet.objects.create(stock=order.stock, person=person, quantity=quantity, average_price=average_price)
        return current_wallet

    def get_quantity(self, stock, person):
        try:
            wallet = Wallet.objects.get(stock=stock, person=person)
            return wallet.quantity
        except:
            return 0