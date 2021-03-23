from datetime import datetime
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import re
import pymysql


id_tab1_list = ['bx_3218110189_1492', 'bx_3218110189_1491', 'bx_3218110189_1490', 'bx_3218110189_1489',
                'bx_3218110189_1488', 'bx_3218110189_1478', 'bx_3218110189_1477', 'bx_651765591_1500',
                'bx_651765591_1499', 'bx_651765591_1498', 'bx_651765591_1497', 'bx_651765591_1496',
                'bx_651765591_1495', 'bx_651765591_1494', 'bx_651765591_1493', 'bx_1373509569_1501',
                'bx_3485106786_1504', 'bx_3485106786_1503', 'bx_3485106786_1502']
id_tab2_list = ['bx_3099439860_1511', 'bx_3099439860_1510', 'bx_3099439860_1509', 'bx_3099439860_1508',
                'bx_3099439860_1507', 'bx_3099439860_1506', 'bx_3099439860_1505', 'bx_565502798_1519',
                'bx_565502798_1518', 'bx_565502798_1517', 'bx_565502798_1516', 'bx_565502798_1515',
                'bx_565502798_1514', 'bx_565502798_1513', 'bx_565502798_1512', 'bx_1454625752_1523',
                'bx_1454625752_1522', 'bx_1454625752_1521']


def get_html(url):
    r = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    return r.text


def write_in_sql(data):
    connect = pymysql.connect(host='localhost', user='', password='', db='', charset='utf8')
    cursor = connect.cursor()
    write_sql = '''INSERT INTO Pshenitsa (Ad, Price, Region, Date, Link) VALUES ('%s', '%s', '%s', '%s', '%s')''' % \
                (data['product'], data['price'], data['city'], data['date'], data['link'])
    cursor.execute(write_sql)
    connect.commit()
    connect.close()


def parser_html(html):
    soup = BeautifulSoup(html, 'lxml')
    for line in id_tab1_list:
        ads = soup.find_all('tr', id=line)

        for ad in ads:
            find_first_price = ad.find('td').find_next('td').find_next('td').find_next('td').find_next('td').text
            get_first_price = re.sub('\W+', '', find_first_price)
            if get_first_price.isdigit():
                nds = int(int(get_first_price) * 20 / 100)
                get_price = float((int(get_first_price) - nds) / 1000)
                price = '%0.2f' % get_price + 'руб/кг.'
                product = 'пшеница 5 класс'
                city = ad.find('td').text.rstrip().lstrip()
                date = datetime.strftime(datetime.today(), '%d.%m.%Y')
                info = {'product': product, 'price': price, 'city': city, 'date': date, 'link': 'sodrugestvo.ru'}
                write_in_sql(info)
                # print(info)

            find_second_price = ad.find('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next(
                'td').find_next('td').text
            get_second_price = re.sub('\W+', '', find_second_price)
            if not get_second_price.isdigit():
                nds_second = int(int(get_second_price) * 20 / 100)
                _get_second_price = float((int(get_second_price) - nds_second) / 1000)
                second_price = '%0.2f' % _get_second_price + 'руб/кг.'
                product = 'пшеница 4 класс'
                city = ad.find('td').text.rstrip().lstrip()
                date = datetime.strftime(datetime.today(), '%d.%m.%Y')
                info = {'product': product, 'price': second_price, 'city': city, 'date': date, 'link': 'sodrugestvo.ru'}
                write_in_sql(info)
                # print(info)

            find_third_price = ad.find('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next(
                'td').find_next('td').find_next('td').find_next('td').text
            get_third_price = re.sub('\W+', '', find_third_price)
            if not get_third_price.isdigit():
                nds_third = int(int(get_third_price) * 20 / 100)
                _get_third_price = float((int(get_third_price) - nds_third) / 1000)
                third_price = '%0.2f' % _get_third_price + 'руб/кг.'
                product = 'пшеница 4 класс'
                city = ad.find('td').text.rstrip().lstrip()
                date = datetime.strftime(datetime.today(), '%d.%m.%Y')
                info = {'product': product, 'price': third_price, 'city': city, 'date': date, 'link': 'sodrugestvo.ru'}
                write_in_sql(info)
                # print(info)

    for line in id_tab2_list:
        ads = soup.find_all('tr', id=line)

        for ad in ads:
            find_first_price = ad.find('td').find_next('td').find_next('td').find_next('td').find_next('td').text
            get_first_price = re.sub('\W+', '', find_first_price)
            if get_first_price.isdigit():
                nds = int(int(get_first_price) * 20 / 100)
                get_price = float((int(get_first_price) - nds) / 1000)
                price = '%0.2f' % get_price + 'руб/кг.'
                product = 'пшеница 3 класс'
                city = ad.find('td').text.rstrip().lstrip()
                date = datetime.strftime(datetime.today(), '%d.%m.%Y')
                info = {'product': product, 'price': price, 'city': city, 'date': date, 'link': 'sodrugestvo.ru'}
                write_in_sql(info)
                # print(info)

            find_second_price = ad.find('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next(
                'td').find_next('td').text
            get_second_price = re.sub('\W+', '', find_second_price)
            if not get_second_price.isdigit():
                nds_second = int(int(get_second_price) * 20 / 100)
                _get_second_price = float((int(get_second_price) - nds_second) / 1000)
                second_price = '%0.2f' % _get_second_price + 'руб/кг.'
                product = 'пшеница 3 класс'
                city = ad.find('td').text.rstrip().lstrip()
                date = datetime.strftime(datetime.today(), '%d.%m.%Y')
                info = {'product': product, 'price': second_price, 'city': city, 'date': date, 'link': 'sodrugestvo.ru'}
                write_in_sql(info)
                # print(info)

            find_third_price = ad.find('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next(
                'td').find_next('td').find_next('td').find_next('td').text
            get_third_price = re.sub('\W+', '', find_third_price)
            if not get_third_price.isdigit():
                nds_third = int(int(get_third_price) * 20 / 100)
                _get_third_price = float((int(get_third_price) - nds_third) / 1000)
                third_price = '%0.2f' % _get_third_price + 'руб/кг.'
                product = 'пшеница 3 класс'
                city = ad.find('td').text.rstrip().lstrip()
                date = datetime.strftime(datetime.today(), '%d.%m.%Y')
                info = {'product': product, 'price': third_price, 'city': city, 'date': date, 'link': 'sodrugestvo.ru'}
                write_in_sql(info)
                # print(info)


def main():
    url = 'https://sodrugestvo.ru/price-list/'

    parser_html(get_html(url))


if __name__ == '__main__':
    main()
