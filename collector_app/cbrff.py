import requests
import xml.etree.ElementTree as ET

from collector_app.modelsPy import ValCurs, Valute


def parse_xml(xml_data):
    tree = ET.ElementTree(ET.fromstring(xml_data))
    root = tree.getroot()

    valutes = []
    for valute_elem in root.findall('Valute'):
        valute_data = {
            'ID': valute_elem.get('ID', ''),
            'NumCode': int(valute_elem.find('NumCode').text),
            'CharCode': valute_elem.find('CharCode').text,
            'Nominal': int(valute_elem.find('Nominal').text),
            'Name': valute_elem.find('Name').text,
            'Value': float(valute_elem.find('Value').text.replace(',', '.')),
            'VunitRate': float(valute_elem.find('VunitRate').text.replace(',', '.'))
        }
        valutes.append(valute_data)

    curs_data = {
        'Date': root.attrib['Date'],
        'name': root.attrib['name'],
        'Valute': valutes
    }

    return curs_data


def get_list_price(date):
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching account info: {e}")
        return None

def get_single_price(symbol, val_curs:ValCurs) -> Valute:

    for curs in val_curs.Valute:
        if curs.CharCode == symbol:
           return curs
