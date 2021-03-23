from datetime import datetime
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import re
import pymysql


id_tab3_list = ['bx_3322728009_1530', 'bx_3322728009_1529', 'bx_3322728009_1528', 'bx_3322728009_1527',
                'bx_3322728009_1526', 'bx_3322728009_1525', 'bx_3322728009_1524', 'bx_2970353375_1538',
                'bx_2970353375_1537', 'bx_2970353375_1536', 'bx_2970353375_1535', 'bx_2970353375_1534',
                'bx_2970353375_1533', 'bx_2970353375_1532', 'bx_2970353375_1531', 'bx_719294866_1575',
                'bx_1574478084_1578', 'bx_1574478084_1577', 'bx_1574478084_1576']


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
    for line in id_tab3_list:
        ads = soup.find_all('tr', id=line)

        for ad in ads:
            find_first_price = ad.find('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').text
            find_price = re.sub('\W+', '', find_first_price)
            if find_price.isdigit():
                get_price = float(int(find_price) / 1000)
                price = '%0.2f' % get_price + 'руб/кг.'
                product = 'горох'
                city = ad.find('td').text.rstrip().lstrip()
                date = datetime.strftime(datetime.today(), '%d.%m.%Y')
                info = {'product': product, 'price': price, 'city': city, 'date': date, 'link': 'sodrugestvo.ru'}
                write_in_sql(info)
                # print(info)


def main():
    url = 'https://sodrugestvo.ru/price-list/'

    parser_html(get_html(url))


if __name__ == '__main__':
    main()
