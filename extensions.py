import requests
import json
from config import keys

# собственный обработчик исключений
class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    # полечение валюты и количества нужного типа данных
    def get_price(base: str, quote: str, amount: int):
        # обработка введения одной валюты дважды
        if base == quote:
            raise ConvertionException(f"Error when exchanging the same currency *{base}*.")

        # обработка неверного введения валюты
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f"Failed to process currency *{base}*")

        # обработка неверного введения валюты
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f"Failed to process currency *{quote}*")

        # обработка неверного введения количества
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Failed to process the amount of *{amount}*")

        # парсинг данных с API сайта, вставляем наши переменные
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}")
        # получаем необходимую валюту
        total_base = json.loads(r.content)[keys[quote]]
        # считаем количество валюты, которое ввел пользователь
        final_amount = round(total_base * amount, 3)
        # возвращаем посчитанное количество валюты
        return final_amount