from datetime import datetime, timezone, time

import requests

from auth_account.auth import Auth
from auth_account.modelsPy import MarketSchedule


def is_within_now():

    # Получаем текущее время
    now = datetime.utcnow()

    start_time = time(5, 10)  # 5:00 утра
    end_time = time(23, 59)  # 12:00 вечера

    # Проверяем, находится ли текущее время в указанных пределах
    return start_time <= now.time() <= end_time



class GetSchedule():
    def __init__(self, auth:Auth):
        self.auth:Auth = auth

    def get_schedule(self, symbol) -> MarketSchedule | None:

        url = f"https://api.finam.ru/v1/assets/{symbol}/schedule"

        headers = {
            "Authorization": self.auth.jwt_token
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Поднимает исключение, если запрос завершился ошибкой
            schedule = response.json()  # Получаем JSON-ответ
            return MarketSchedule.model_validate(schedule)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching account info: {e}")
            return None




    def is_market_open_now(self, symbol) -> bool:

        schedule = self.get_schedule(symbol)
        if schedule is None:
            return False

        if schedule is None:
            return False

        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        # Проверяем каждую сессию
        for session in schedule.sessions:
            if session.interval.start_time <= now <= session.interval.end_time:
                if session.type == 'EARLY_TRADING' or session.type == 'CORE_TRADING' or session.type == 'LATE_TRADING':
                    return True

        return False

