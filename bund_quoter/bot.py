from typing import List, Optional

import requests

from auth_account.auth import Auth
from bund_quoter.models import BotQuoter
from bund_quoter.modelsPy import Order


class Bot():
    def __init__(self, auth:Auth, bot:BotQuoter):

        self.bot: BotQuoter = bot
        self.auth: Auth = auth
        self.account_id = auth.account_id
        self.jwt_token = auth.jwt_token


    def get_assets(self):

        url = f"https://api.finam.ru/v1/assets/{self.bot.symbol}/params?account_id={self.account_id}"

        headers = {
            "Authorization": self.jwt_token
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Поднимает исключение, если запрос завершился ошибкой
            info = response.json()  # Получаем JSON-ответ
            return info
        except requests.exceptions.RequestException as e:
            print(f"Error fetching account info: {e}")
            return None

    def get_last_quote(self) -> dict:

        url = f"https://api.finam.ru/v1/instruments/{self.bot.symbol}/quotes/latest"

        headers = {
            "Authorization": self.jwt_token
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Поднимает исключение, если запрос завершился ошибкой
            quote = response.json()  # Получаем JSON-ответ
            return quote
        except requests.exceptions.RequestException as e:
            print(f"Error fetching account info: {e}")
            return {}

    def setInfo(self):

        assets = self.get_assets()
        # print(assets)
        if assets and 'tradeable' in assets:
            self.is_assets = assets.get('tradeable', False)

        if self.is_assets == False: return None

        info = self.auth.account_info

        side = 'n'
        value = 0
        positions = info.get('positions', [])

        for position in positions:
            if self.bot.symbol == position.get('symbol', ''):
                value = position.get('quantity', {}).get('value', 0)

        if value > 0:
            side = 'b'
        if value < 0:
            side = 's'

        if value:
            value = abs(value)

        BotQuoter.objects.filter(id=self.bot.id).update(side=side, value=value)

    def setQuote(self):

        quote = self.get_last_quote()
        if quote and 'symbol' in quote and quote.get('symbol') == self.bot.symbol:
            ask = quote.get('quote', {}).get('ask', {}).get('value', 0)
            last = quote.get('quote', {}).get('last', {}).get('value', 0)
            bid = quote.get('quote', {}).get('bid', {}).get('value', 0)

            BotQuoter.objects.filter(id=self.bot.id).update(ask=ask, last=last, bid=bid)

        try:
            self.bot = BotQuoter.objects.get(id=self.bot.id)
        except BotQuoter.DoesNotExist:
            pass

    def get_orders(self) -> List[Order]:

        orders_list: List[Order] = []
        orders = self.auth.orders
        for order in orders:
            if self.bot.symbol == order.symbol:
                orders_list.append(order)

        return orders_list

    def place_order(self, side, limit_price, quantity)-> Optional[Order]:

        symbol = self.bot.symbol

        account_id = self.account_id

        url = f"https://api.finam.ru/v1/accounts/{account_id}/orders"

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.jwt_token
        }
        data = {

            "symbol": symbol,
            "quantity": {
                "value": str(quantity)
            },
            "side": side,
            "type": "ORDER_TYPE_LIMIT",
            "timeInForce": "TIME_IN_FORCE_DAY",
            "limitPrice": {
                "value": str(limit_price)
            },
            "stopCondition": "STOP_CONDITION_UNSPECIFIED",
            "legs": []
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            ord = response.json()
            order_id = ord.get('order_id', '')
            status = ord.get('status', '')
            order = ord.get('order', {})
            account_id = order.get('account_id', '')
            symbol = order.get('symbol', '')
            side = order.get('side', '')
            order_type = order.get('type', '')
            limit_price = float(order.get('limit_price', {}).get('value', 0))
            quantity = float(order.get('quantity', {}).get('value', 0))

            return Order(
                        order_id=order_id,
                        account_id=account_id,
                        symbol=symbol,
                        side=side,
                        status=status,
                        order_type=order_type,
                        limit_price=limit_price,
                        quantity=quantity
                    )
        else:
            # Обработка ошибок
            print(f"Ошибка: {response.status_code}, {response.text}")
            return None

    def cancel_order(self, order_id):

        account_id = self.account_id

        url = f"https://api.finam.ru/v1/accounts/{account_id}/orders/{order_id}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.jwt_token
        }

        response = requests.delete(url, headers=headers)

        if response.status_code == 200:

            return response.json()

        else:
            # Обработка ошибок
            print(f"Ошибка: {response.status_code}, {response.text}")
            return None
