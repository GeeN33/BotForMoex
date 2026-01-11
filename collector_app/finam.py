import requests

from collector_app.modelsPy import Quote


def get_last_quote(jwt_token, symbol) -> Quote | None:

    url = f"https://api.finam.ru/v1/instruments/{symbol}/quotes/latest"

    headers = {
        "Authorization": jwt_token
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Поднимает исключение, если запрос завершился ошибкой
        quote = response.json()  # Получаем JSON-ответ

        ask = quote.get('quote', {}).get('ask', {}).get('value', 0)
        last = quote.get('quote', {}).get('last', {}).get('value', 0)
        bid = quote.get('quote', {}).get('bid', {}).get('value', 0)

        return Quote(ask=ask, last=last, bid=bid)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching account info: {e}")
        return None
