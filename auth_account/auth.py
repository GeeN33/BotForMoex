from datetime import datetime, timedelta
from typing import List

import requests

from auth_account.models import BotAuth
from bund_quoter.modelsPy import Order

class Auth:
    def __init__(self, account_id):

        self.account_id = account_id
        self.jwt_token = None
        self.is_active = False
        self.auth_bot: BotAuth
        self.account_info: dict = {}
        self.orders: List[Order] = []

        try:
            self.auth_bot = BotAuth.objects.get(account_id=account_id)
        except BotAuth.DoesNotExist:
            return

        token_details = self.get_token_details(self.auth_bot.jwt_token)

        if token_details and token_details.get('expires_at') and self.is_token_valid(token_details):
            self.jwt_token = self.auth_bot.jwt_token
            self.is_active = True
            # print('token_details old')
        else:
            self.jwt_token = self.get_jwt_token(self.auth_bot.secret_key)
            if self.jwt_token:
                BotAuth.objects.filter(id=self.auth_bot.id).update(jwt_token=self.jwt_token)
                self.is_active = True
                # print('token_details new')
            else:
                self.is_active = False
                # print('token_details error')

    def get_jwt_token(self, secret_key) -> str | None:
        url = "https://api.finam.ru/v1/sessions"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "secret": secret_key
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            response_json = response.json()
            # Извлечение JWT токена из ответа
            if response_json and "token" in  response_json:
                 token = response_json.get("token")
                 return token
            else:
                return None
        else:
            # Обработка ошибок
            print(f"Ошибка: {response.status_code}, {response.text}")
            return None
    def is_token_valid(self, token_info) -> bool:
        # Преобразуем время из строки в объект datetime
        expires_at = datetime.strptime(token_info['expires_at'], '%Y-%m-%dT%H:%M:%SZ')

        # Получаем текущее время в UTC
        current_time = datetime.utcnow()

        # print(expires_at - current_time)

        five_minutes = timedelta(minutes=5)
        # Сравниваем текущее время с временем истечения
        return current_time < (expires_at - five_minutes)
    def get_token_details(self, jwt_token) -> dict:
        url = "https://api.finam.ru/v1/sessions/details"

        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "token": jwt_token
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            token = response.json()
            return token
        else:
            return {}
    def get_account_info(self) -> None:

        url = f"https://api.finam.ru/v1/accounts/{self.account_id}"

        headers = {
            "Authorization": self.jwt_token
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Поднимает исключение, если запрос завершился ошибкой
            account_info = response.json()  # Получаем JSON-ответ
            self.account_info = account_info
        except requests.exceptions.RequestException as e:
            print(f"Error fetching account info: {e}")
            self.account_info = {}

    def get_orders(self) -> None:

        url = f"https://api.finam.ru/v1/accounts/{self.account_id}/orders"

        headers = {
            "Authorization": self.jwt_token
        }

        orders_list: List[Order] = []
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Поднимает исключение, если запрос завершился ошибкой
            account_info = response.json()  # Получаем JSON-ответ
            orders = account_info.get('orders', [])
            # print(orders)
            for ord in orders:
                order_id = ord.get('order_id', '')
                status = ord.get('status', '')
                order = ord.get('order', {})
                if self.auth_bot.account_id == order.get('account_id', ''):
                    account_id = order.get('account_id', '')
                    symbol = order.get('symbol', '')
                    side = order.get('side', '')
                    order_type = order.get('type', '')
                    limit_price = float(order.get('limit_price', {}).get('value', 0))
                    quantity = float(order.get('quantity', {}).get('value', 0))
                    orders_list.append(
                        Order(
                            order_id=order_id,
                            account_id=account_id,
                            symbol=symbol,
                            side=side,
                            status=status,
                            order_type=order_type,
                            limit_price=limit_price,
                            quantity=quantity
                        ))

            self.orders = orders_list

        except requests.exceptions.RequestException as e:
            print(f"Error fetching account info: {e}")
            return None
