from typing import List

from auth_account.auth import Auth
from bund_quoter.bot import Bot
from bund_quoter.models import BotQuoter

from bund_quoter.modelsPy import Order
from bund_quoter.utils import is_within_schedule


# python manage.py start_bot_test

def runBotOne(account_info: dict, orders: List[Order], auth:Auth, botQ: BotQuoter):
    if not is_within_schedule(): return
    bot = Bot(auth, botQ)



def startBotQuoter():

    auth = Auth('1191032')
    auth.get_account_info()
    auth.get_orders()
    if not auth.is_active: return

    account_info = auth.account_info
    orders = auth.orders

    bots = BotQuoter.objects.filter(auth_bot_id=auth.auth_bot.id, is_active=True)
    for botQ in bots:
        runBotOne(account_info, orders, auth, botQ)



