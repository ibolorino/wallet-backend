import requests
import json
from wallet.settings import API_KEY
from django.utils import timezone
from .models import *

api_key = API_KEY
url = 'https://www.alphavantage.co/query?'


def update_price(stock):

    stocks = Stock.objects.filter(ticker=stock.ticker)
    last_update = stock.last_update
    dif = 0
    update_date = timezone.now()
    if last_update:
        dif = (update_date - last_update).total_seconds()

    if dif > 900 or not last_update:

        api_dict = {
            'function' : 'GLOBAL_QUOTE',
            'symbol' : stock.ticker + '.SAO',
            'apikey': api_key,
        }

        api_url = url + "&".join(k + "=" + v for k, v in api_dict.items())

        response = requests.get(api_url).json()['Global Quote']

        new_price = float(response['05. price'])

        stocks.update(last_update=update_date, current_value=new_price)
    
        return update_date, new_price
    return