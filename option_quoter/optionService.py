from typing import Optional

import requests

from option_quoter.modelsPy import OptionBrief


class OptionService:
    def __init__(self):
        self.base_url = 'https://iss.moex.com/iss/apps/option-calc/v1'

    def get_option(self, asset_code: str, secid: str) -> Optional[OptionBrief]:

        url = f"{self.base_url}/assets/{asset_code}/options/{secid}"

        try:
            response = requests.get(url)

            return OptionBrief.model_validate(response.json())

        except Exception as e:
            print('Ошибка при загрузке страницы: ' + str(e))
            return None

    def get_assets(self):

        url = f"{self.base_url}/assets/"

        try:
            response = requests.get(url)

            return response.json()

        except Exception as e:
            print('Ошибка при загрузке страницы: ' + str(e))
            return None