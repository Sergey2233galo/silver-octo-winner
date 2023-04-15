import json
import requests
from config import exchanges, headers

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта '{base}' не найдена.")
        try:
            quote_key = exchanges[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта '{quote}' не найдена.")
        if base_key == quote_key:
            raise APIException(f"Невозможно перевести одинаковые валюты: {base}")
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество '{amount}'")

        r = requests.get(f'https://api.apilayer.com/exchangerates_data/latest?symbols={quote_key}&base={base_key}', headers=headers)
        resp = json.loads(r.content)
        new_price = round((resp['rates'][quote_key] * amount), 3)
        message = f"Цена {amount} {base} в {quote} : {new_price}"
        return message

