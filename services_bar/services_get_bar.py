from datetime import datetime, timedelta
from time import sleep
from typing import List, Optional, Dict

import requests

from auth_account.auth import Auth
from services_bar.modelsBars import DataModel, BarModel, BarPair, StockModel


class GetBars():
    def __init__(self, auth: Auth, symbolA, symbolB, symbolC):
        self.auth = auth
        self.timeframe = 'TIME_FRAME_H1'
        self.periodDays = 7
        self.periodEma = 21

        self.symbolA = symbolA
        self.symbolB = symbolB
        self.symbolC = symbolC


    def get_last_quote(self, symbol) -> Optional[StockModel]:

        url = f"https://api.finam.ru/v1/instruments/{symbol}/quotes/latest"

        headers = {
            "Authorization": self.auth.jwt_token
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Поднимает исключение, если запрос завершился ошибкой
            quote = response.json()  # Получаем JSON-ответ
            return StockModel.model_validate(quote)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching account info: {e}")
            return None

    def get_bars(self, symbol, start_time, end_time, timeframe)-> Optional[List[BarModel]] :

        url = f"https://api.finam.ru/v1/instruments/{symbol}/bars?interval.start_time={start_time}&interval.end_time={end_time}&timeframe={timeframe}"

        headers = {
            "Authorization": self.auth.jwt_token
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Поднимает исключение, если запрос завершился ошибкой
            data = response.json()  # Получаем JSON-ответ
            dataModel = DataModel.model_validate(data)
            return dataModel.bars
        except requests.exceptions.RequestException as e:
            print(f"Error fetching account info: {e}")
            return []

    def get_bars_dict(self, symbol, start_time, end_time, timeframe) -> Dict[datetime, BarModel]:

        barsDict: Dict[datetime, BarModel] = {}

        bars = self.get_bars(symbol, start_time, end_time, timeframe)

        for bar in bars:
            barsDict[bar.timestamp] = bar

        return barsDict

    def get_bars_Pair(self, bars1: Dict[datetime, BarModel],  bars2: Dict[datetime, BarModel]) -> Dict[datetime, BarPair]:

        barsDict: Dict[datetime, BarPair] = {}

        for k, bar1 in bars1.items():
            bar2 = bars2.get(k)
            if bar2:
                close = bar2.close.value - bar1.close.value
                barsDict[k] = BarPair(timestamp=k, close=close)

        return barsDict

    def ema_by_close(self, bars: Dict[datetime, BarPair], period: int) -> Dict[datetime, BarPair]:
        if not bars or period <= 0:
            return bars

        sorted_dates = sorted(bars.keys())

        if len(sorted_dates) < period:
            return bars

        # Коэффициент сглаживания
        alpha = 2 / (period + 1)
        ema_prev = 0

        # Старт: SMA за первый период
        sum_close = sum(bars[date].close for date in sorted_dates[:period])
        ema_prev = sum_close / period
        bars[sorted_dates[period - 1]].ema = ema_prev

        # Дальше обычная формула EMA
        for i in range(period, len(sorted_dates)):
            date = sorted_dates[i]
            price = bars[date].close
            ema = alpha * price + (1 - alpha) * ema_prev
            bars[date].ema = ema
            ema_prev = ema

        return bars

    def get_Pair_Plus_Pair(self, bars1: Dict[datetime, BarPair],  bars2: Dict[datetime, BarPair]) -> Dict[datetime, BarPair]:

        barsDict: Dict[datetime, BarPair] = {}

        for k, bar1 in bars1.items():
            bar2 = bars2.get(k)
            if bar2:
                close = bar2.close - bar1.close
                ema = bar2.ema - bar1.ema
                barsDict[k] = BarPair(timestamp=k, close=close, ema=ema)

        return barsDict

    def set_Pair_Data(self) -> Optional[BarPair]:

        # Текущая дата и время
        now = datetime.utcnow()
        #
        # # Начальное время: текущее время минус n дней
        start_time = now - timedelta(days=self.periodDays)

        # Конечное время: текущая дата и время
        end_time = now + timedelta(days=1)
        #
        # # Форматирование времени в строку с форматом ISO 8601
        start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_time = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')



        barsA = self.get_bars_dict(self.symbolA, start_time, end_time, self.timeframe)
        if not barsA: return None

        sleep(1)
        barsB = self.get_bars_dict(self.symbolB, start_time, end_time, self.timeframe)
        if not barsB: return None

        sleep(1)
        barsC = self.get_bars_dict(self.symbolC, start_time, end_time, self.timeframe)
        if not barsC: return None

        barsBA = self.get_bars_Pair(barsA, barsB)
        barsCA = self.get_bars_Pair(barsA, barsC)

        barsBA = self.ema_by_close(barsBA, self.periodEma)
        barsCA = self.ema_by_close(barsCA, self.periodEma)

        barsCB = self.get_Pair_Plus_Pair(barsBA, barsCA)

        if not barsCB: return None

        last_key = list(barsCB.keys())[-1]

        return barsCB[last_key]
