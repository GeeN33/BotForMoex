from datetime import datetime, timedelta
from time import sleep

from collector_app.cbrff import get_list_price, parse_xml, get_single_price
from collector_app.models import ValuteCursCbr, BarCbrDay
from collector_app.modelsPy import ValCurs


# bar_cbr_day_test

def run_bar_cbr_day():
    for i in range(1, 0, -1):

            sleep(5)

            today = datetime.today()

            today = today + timedelta(days = i * -1)

            datetime_today = datetime.combine(today, datetime.min.time())

            timestamp_today = int(datetime_today.timestamp())

            formatted_date_long = today.strftime('%y%m%d')

            formatted_date = today.strftime('%d/%m/%Y')

            xml_data = get_list_price(formatted_date)
            parsed_data = parse_xml(xml_data)
            val_curs = ValCurs(**parsed_data)

            timestamp = timestamp_today
            date_str = formatted_date_long

            year = today.year
            month = today.month
            day = today.day

            valuteCursCbrs = ValuteCursCbr.objects.filter(is_active=True)
            for valute in valuteCursCbrs:
                    prices = get_single_price(valute.name, val_curs)
                    if prices:
                         barCbr = BarCbrDay.objects.get_or_create(cbr=valute, timestamp=timestamp)[0]
                         barCbr.date_str = date_str
                         barCbr.year = year
                         barCbr.month = month
                         barCbr.day = day
                         barCbr.price = prices.Value
                         barCbr.save()

                         item = f'{timestamp} {valute.name}; {date_str}; {prices.Value}    {year} {month} {day}'
                         print(item)
