import requests
import json
from config import keys_currency

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException('Невозможно перевести одинаковые валюты', base)

        try:
            quote_ticker = keys_currency[quote]
        except KeyError:
            raise APIException('Не удалось обработать валюту ', quote)

        try:
            base_ticker = keys_currency[base]
        except KeyError:
            raise APIException('Не удалось обработать валюту ', base)

        try:
            amount = float(amount)
        except ValueError:
            raise APIException('Не удалось обработать количество ', amount)

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')

        return json.loads(r.content)[keys_currency[base]] * amount


