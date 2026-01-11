from datetime import datetime, time, timedelta
from typing import List, Optional

import pytz


def is_within_schedule():
    # Устанавливаем часовой пояс для Москвы
    moscow_tz = pytz.timezone('Europe/Moscow')

    # Получаем текущее время в московском часовом поясе
    now = datetime.now(moscow_tz)

    # Дни недели: 0 - понедельник, 1 - вторник, ..., 5 - суббота, 6 - воскресенье
    weekday = now.weekday()

    # Устанавливаем временные рамки для будних дней и выходных
    if weekday < 5:  # Если это будний день
        start_time = time(10, 1) # 9:00 утра
        end_time = time(18, 45)  # 6:59 ночи (практически 9:00)
    else:  # Если это выходной (суббота или воскресенье)
        return False

    # Проверяем, находится ли текущее время в указанных пределах
    return start_time <= now.time() <= end_time