import csv
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pymysql

headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application'
                     '/signed-exchange;v=b3;q=0.9',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.'
                         '3945.130 Safari/537.36'}

url_ads_buy_list = []
url_ads_sell_list = []


def get_html(url, headers):
    r = requests.get(url, headers=headers)
    return r.text


# def write_csv(data):
#     name_file = 'rynok_apk_Pshenitsa.csv'
#     with open(name_file, 'a', errors='ignore', newline='') as file:
#         writer = csv.writer(file, delimiter=';')
#         writer.writerow((data['product'], data['price'], data['city'], data['date']))


def write_in_sql(data):
    connect = pymysql.connect(host='localhost', user='', password='', db='', charset='utf8')
    cursor = connect.cursor()
    write_sql = '''INSERT INTO Pshenitsa (Ad, Price, Region, Date) VALUES ('%s', '%s', '%s', '%s')''' % \
                (data['product'], data['price'], data['city'], data['date'])
    cursor.execute(write_sql)
    connect.commit()
    connect.close()


def get_urls_ads_buy(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = soup.find('ul', class_='ads').find_all('a')
    for url in urls:
        url_ad = url.get('href')
        only_url_ad = re.search('^/buy', url_ad)
        if only_url_ad is not None:
            url_ads_buy_list.append('https://rynok-apk.ru' + url_ad)


def get_urls_ads_sell(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = soup.find('ul', class_='ads').find_all('a')
    for url in urls:
        url_ad = url.get('href')
        only_url_ad = re.search('^/sell', url_ad)
        if only_url_ad is not None:
            url_ads_sell_list.append('https://rynok-apk.ru' + url_ad)


def parser_html(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find_all('div', class_='item')

    for ad in ads:
        try:
            price = ad.find('var', itemprop='price').text.split()
            if len(price) > 1:
                get_digits = price[0] + price[1]
                get_price = float(int(get_digits) / 1000)
                price = '%.02f' % get_price + 'руб/кг.'
                # print(price)
            if len(price) == 1:
                get_digits = str(price).replace('[', '').replace(']', '').replace("'", '')
                price = '%.02f' % int(get_digits) + 'руб/кг.'
                # print(price)
        except:
            price = ''

        if price != '':
            message = ad.find('article', itemprop='description').text
            find_product = re.search('(пшеница)', message)
            if find_product is not None:
                product = 'пшеница'
                # print(product)

                find_date = ad.find('p', class_='time').find('time').get('datetime').split()
                get_date = find_date[0].replace('-', '.')
                date = datetime.strptime(get_date, '%Y.%m.%d').strftime('%d.%m.%Y')
                # print(date)

                find_city = ad.find('span', class_='adv-areas').text.split(',')
                city = find_city[0]
                # print(city)

                info = {'product': product, 'price': price, 'date': date, 'city': city}
                # write_csv(info)
                write_in_sql(info)


def buy():
    url = 'https://rynok-apk.ru/billboard/buy-zernovye-plants/pshenitsa/'
    get_urls_ads_buy(get_html(url, headers))
    url_ads_buy_set = set(url_ads_buy_list)
    for url in url_ads_buy_set:
        parser_html(get_html(url, headers))


def sell():
    url = 'https://rynok-apk.ru/billboard/zernovye-plants/pshenitsa/'
    get_urls_ads_sell(get_html(url, headers))
    url_ads_sell_set = set(url_ads_sell_list)
    for url in url_ads_sell_set:
        parser_html(get_html(url, headers))


def main():
    buy()
    sell()


if __name__ == '__main__':
    main()
