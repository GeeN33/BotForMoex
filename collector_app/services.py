from datetime import datetime, timedelta, time
from time import sleep
from zoneinfo import ZoneInfo

from auth_account.auth import Auth
from collector_app.cbrff import parse_xml, get_list_price, get_single_price
from collector_app.finam import get_last_quote
from collector_app.models import ValuteCursCbr, CollectorQuoter, Bar, BarCbr, BarCbrDay
from collector_app.modelsPy import ValCurs, Quote
from collector_app.utils import is_within_schedule


# start_collector_test

def run_cbr_day(today:datetime, valute: ValuteCursCbr, prices):

    utc = ZoneInfo("UTC")
    datetime_today = datetime.combine(today, time.min).replace(tzinfo=utc)

    timestamp_today = int(datetime_today.timestamp())
    timestamp = timestamp_today
    date_str = today.strftime('%y%m%d')

    year = today.year
    month = today.month
    day = today.day

    barCbr = BarCbrDay.objects.get_or_create(cbr=valute, timestamp=timestamp)[0]
    barCbr.date_str = date_str
    barCbr.year = year
    barCbr.month = month
    barCbr.day = day
    barCbr.price = prices
    barCbr.save()



def startCursCbr():
    today = datetime.today()
    formatted_date = today.strftime('%d/%m/%Y')

    xml_data = get_list_price(formatted_date)
    parsed_data = parse_xml(xml_data)
    val_curs = ValCurs(**parsed_data)

    valuteCursCbrs = ValuteCursCbr.objects.filter(is_active=True)
    for valute in valuteCursCbrs:
        price = get_single_price(valute.name, val_curs)
        if price:
            valute.nominal=price.Nominal
            valute.value = price.Value
            valute.save()


def startCursCbrPlusDay():

    today = datetime.today()

    today2 = today + timedelta(days=1)

    formatted_date = today2.strftime('%d/%m/%Y')

    xml_data = get_list_price(formatted_date)
    parsed_data = parse_xml(xml_data)
    val_curs = ValCurs(**parsed_data)

    valuteCursCbrs = ValuteCursCbr.objects.filter(is_active=True)
    for valute in valuteCursCbrs:
        price = get_single_price(valute.name, val_curs)
        if price:
            barCbr = BarCbr.objects.create(cbr=valute)
            bar = Bar.objects.filter(collector__cbr=valute).last()
            if bar:
                barCbr.last = bar.last2

            barCbr.day1 = today.day
            barCbr.hour1 = today.hour
            barCbr.last1 = valute.value

            barCbr.day2 = today2.day
            barCbr.hour2 = today2.hour
            barCbr.last2  = price.Value

            barCbr.save()

            run_cbr_day(today2, valute, price.Value)


def runCollectorOne(auth:Auth, collector: CollectorQuoter):

    quote_bonds = get_last_quote(auth.jwt_token, collector.symbol_bonds)
    quote_futures = get_last_quote(auth.jwt_token, collector.symbol_futures)

    if not quote_bonds or not quote_futures: return

    if quote_bonds.ask == 0 or quote_bonds.last == 0 or quote_bonds.bid == 0: return
    if quote_futures.ask == 0 or quote_futures.last == 0 or quote_futures.bid == 0: return

    cbr_price = collector.cbr.value * collector.nominal_bonds

    quote_bonds = Quote(
        ask = cbr_price * (quote_bonds.ask / 100) if quote_bonds.ask else 0,
        last = cbr_price * (quote_bonds.last / 100) if quote_bonds.last else 0,
        bid = cbr_price * (quote_bonds.bid / 100) if quote_bonds.bid else 0)

    quote_futures = Quote(
        ask = quote_futures.ask * collector.nominal_futures if quote_bonds.last else 0,
        last = quote_futures.last * collector.nominal_futures if quote_bonds.last else 0,
        bid = quote_futures.bid * collector.nominal_futures if quote_bonds.last else 0)


    quote_cpread = Quote(
        ask = quote_bonds.ask - quote_futures.bid ,
        last = quote_bonds.last - quote_futures.last,
        bid = quote_bonds.bid - quote_futures.ask)

    bar = Bar.objects.create(collector=collector)

    bar.cbr_price = collector.cbr.value

    bar.last = quote_cpread.last
    bar.ask = quote_cpread.ask
    bar.bid = quote_cpread.bid

    bar.last1 = quote_bonds.last
    bar.ask1 = quote_bonds.ask
    bar.bid1 = quote_bonds.bid

    bar.last2 = quote_futures.last
    bar.ask2 = quote_futures.ask
    bar.bid2 = quote_futures.bid
    bar.save()

    # print(cbr_price)
    # print(quote_bonds)
    # print(quote_futures)
    # print(quote_cpread)


def startCollectorQuoter():

    if not is_within_schedule(): return 'not within schedule'

    auth = Auth('1191032')
    if not auth.is_active: return 'not active'

    collectors = CollectorQuoter.objects.filter(auth_bot_id=auth.auth_bot.id, is_active=True)
    for collector in collectors:
        sleep(2)
        runCollectorOne(auth, collector)

    return  'ok'