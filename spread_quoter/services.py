from datetime import datetime, timedelta
from time import sleep
from typing import List

from django.db.models import Q

from auth_account.auth import Auth
from auth_account.models import BotAuth
from auth_account.schedule import GetSchedule, is_within_now
from core.utils import round_price, check_pos
from services_bar.services_get_bar import GetBars
from spread_quoter.lib.bot import Bot
from spread_quoter.models import OrderSmartSpread, BotQuoterSpread
from spread_quoter.modelsPy import OrderDetail
from spread_quoter.utils import filter_order, check_order


# python manage.py spread_bot_test
def startSpreadQuoter(bot_name, account_id):
    if is_within_now() == False: return 'not awithin now'

    print('start')
    auth = Auth(account_id)
    if not auth.is_active: return 'not active auth'

    bot = Bot(auth, bot_name)
    if not bot.is_active: return 'not active bot'

    # schedule = GetSchedule(auth)
    # if schedule.is_market_open_now(bot.bot.symbolCB) == False: return 'not schedule bot'

    if not bot.setInfo(): return 'not setInfo bot'

    if not bot.setQuote(): return 'not setQuote bot'

    orders = bot.get_orders()

    print('next')

    step_quantity = bot.bot.step_quantity
    max_quantity = bot.bot.max_quantity
    quantity_current = bot.bot.quantityCB

    # quantityCB = abs(bot.bot.quantityCB)
    # quantityC = abs(bot.bot.quantityC)
    # quantityB = abs(bot.bot.quantityB)

    quantityCB = 10
    quantityC = 0
    quantityB = 10

    step_price = bot.bot.step_price
    ask = bot.bot.ask
    last = bot.bot.last
    bid = bot.bot.bid
    ema = bot.bot.ema


    # <editor-fold desc="Проверка баланса открытых закрытых позиций">
    raz_pos = check_pos(max_quantity, quantity_current)
    if raz_pos:
        print(f'raz_pos {raz_pos}')
        # # Закрыть все ордера
        # for order in orders:
        #     if order.status == 'ORDER_STATUS_NEW' or order.status == 'ORDER_STATUS_PARTIALLY_FILLED':
        #         # print('cancel_order', order)
        #         bot.cancel_order(order.order_id)
        #
        # if quantityC == 0 or quantityB == 0:
        #     if quantityC == 0:
        #         bot.place_order(bot.bot.symbolB,
        #                                 'ORDER_TYPE_MARKET',
        #                                 'SIDE_SELL',
        #                                 0,
        #                                  raz_pos,
        #                                 f'{bot.bot.symbolB}_MARKET')
        #         return f'check_pos {raz_pos} bot'
        #     if quantityB == 0:
        #             bot.place_order(bot.bot.symbolC,
        #                                     'ORDER_TYPE_MARKET',
        #                                     'SIDE_SELL',
        #                                     0,
        #                                     raz_pos,
        #                                     f'{bot.bot.symbolC}_MARKET')
        #             return f'check_pos {raz_pos} bot'
        # elif quantityC > quantityB:
        #     bot.place_order(bot.bot.symbolB,
        #                     'ORDER_TYPE_MARKET',
        #                     'SIDE_SELL',
        #                     0,
        #                     raz_pos,
        #                     f'{bot.bot.symbolB}_MARKET')
        #     return f'check_pos {raz_pos} bot'
        #
        # else:
        #     bot.place_order(bot.bot.symbolC,
        #                     'ORDER_TYPE_MARKET',
        #                     'SIDE_SELL',
        #                     0,
        #                     raz_pos,
        #                     f'{bot.bot.symbolC}_MARKET')
        #     return f'check_pos {raz_pos} bot'
        #
        return f'check_pos {raz_pos} bot'
    # </editor-fold>

    # <editor-fold desc="Обновление цены и объёма уровней">
    OrderSmartSpread.objects.filter(bot_id=bot.bot.id).update(is_active=False)
    s_levels = OrderSmartSpread.objects.filter(bot_id=bot.bot.id, level_side='s').order_by('-level_queue')
    b_levels = OrderSmartSpread.objects.filter(bot_id=bot.bot.id, level_side='b').order_by('-level_queue')
    if len(s_levels) > 0 and quantityCB > quantityC:
        quantityT = quantityCB - quantityC
        for level in s_levels:
            if quantityT > 0:
                if quantityT < step_quantity:
                    level_quantity = quantityT
                    quantityT -= step_quantity
                else:
                    level_quantity = step_quantity
                    quantityT -= step_quantity

                level_price = round_price(ema + (level.level_queue * (level.level_step * step_price)), step_price)
                # print(f'{level.level_queue}: {level_price} _ {level_quantity}')
                OrderSmartSpread.objects.filter(id=level.id).update(level_price=level_price, level_quantity=level_quantity, is_active=True)
    if len(b_levels) > 0 and quantityCB > quantityB:
        quantityT = quantityCB - quantityB
        for level in b_levels:
            if quantityT > 0:
                if quantityT < step_quantity:
                    level_quantity = quantityT
                    quantityT -= step_quantity
                else:
                    level_quantity = step_quantity
                    quantityT -= step_quantity

                level_price = round_price(ema - (level.level_queue * (level.level_step * step_price)), step_price)
                # print(f'{level.level_queue}: {level_price} _ {level_quantity}')
                OrderSmartSpread.objects.filter(id=level.id).update(level_price=level_price, level_quantity=level_quantity, is_active=True)
    # </editor-fold>

    # <editor-fold desc="Фильтрация ордеров которые не подходят по критериям">
    normal_orders: List[OrderDetail] = []
    all_levels = OrderSmartSpread.objects.filter(bot_id=bot.bot.id, is_active=True).order_by('-level_queue')
    for level in all_levels:
        orders, normal_order = filter_order(orders, level.client_order_id, level.level_price, level.level_quantity)
        normal_orders.append(normal_order)
    # </editor-fold>

    # <editor-fold desc="Закрытие старых ордеров которые не прошли фильтрацию">
    # for order in orders:
    #     if order.status == 'ORDER_STATUS_NEW' or order.status == 'ORDER_STATUS_PARTIALLY_FILLED':
    #         # print('cancel_order', order)
    #         bot.cancel_order(order.order_id)
    # </editor-fold>

    # <editor-fold desc="установка новых лимитных ордеров">
    # s_levels = OrderSmartSpread.objects.filter(bot_id=bot.bot.id, level_side='s').order_by('-level_queue')
    # b_levels = OrderSmartSpread.objects.filter(bot_id=bot.bot.id, level_side='b').order_by('-level_queue')
    # for level in s_levels:
    #     if check_order(normal_orders, level.order_id) == False:
    #         order = bot.place_order(bot.bot.symbolCB,
    #                                 'ORDER_TYPE_LIMIT',
    #                                 'SIDE_SELL',
    #                                 level.level_price,
    #                                 level.level_quantity,
    #                                 level.client_order_id)
    #
    #         if order:
    #             OrderSmartSpread.objects.filter(id=level.id).update(
    #                 order_id=order.order_id,
    #                 status = order.status,
    #                 order_type = order.order.type,
    #                 side = order.order.side,
    #                 limit_price = order.order.limit_price,
    #                 quantity = order.order.quantity)
    # for level in b_levels:
    #     if check_order(normal_orders, level.order_id) == False:
    #         order = bot.place_order(bot.bot.symbolCB,
    #                                 'ORDER_TYPE_LIMIT',
    #                                 'SIDE_BUY',
    #                                 level.level_price,
    #                                 level.level_quantity,
    #                                 level.client_order_id)
    #
    #         if order:
    #             OrderSmartSpread.objects.filter(id=level.id).update(
    #                 order_id=order.order_id,
    #                 status=order.status,
    #                 order_type=order.order.type,
    #                 side=order.order.side,
    #                 limit_price=order.order.limit_price,
    #                 quantity=order.order.quantity)
    # </editor-fold>


    all_levels = OrderSmartSpread.objects.filter(bot_id=bot.bot.id, is_active=True).order_by('level_id')
    for level in all_levels:
        print(level)


    return 'run bot ok'


def startSpreadQuoterSingle(symbol):

    bot:BotQuoterSpread = BotQuoterSpread.objects.filter(Q(symbolA=symbol) | Q(symbolB=symbol) | Q(symbolC=symbol) | Q(symbolCB=symbol)).last()

    if bot and bot.auth_bot and bot.auth_bot.account_id:

       startSpreadQuoter(bot.name, bot.auth_bot.account_id)