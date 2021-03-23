from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import re
import pymysql


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
    ads = soup.find_all('div', class_='new-city-block-content')
    city_and_date = soup.find_all('div', class_='tab active')

    for ad in ads:
        information = ad.find('div', class_='tab active').find('table', border='1').find('tbody').find_all(
            'tr')

        for data in information:
            find_price = data.find('td', colspan='1').find_next('td', colspan='1').text.strip()
            get_price = str(re.findall('\d{5}.\d+', find_price)).replace("'", '').replace('[', '').replace(']', '')
            float_price = float(int(get_price.split(',')[0]) / 1000)
            price = '%0.2f' % float_price + 'руб/кг.'
            # print(price)

            find_product = data.find('td', colspan='1').text.lower()
            get_product = re.findall('пшеница.\d.\w+', find_product)
            product = str(get_product).replace("'", '').replace('[', '').replace(']', '')
            # print(product)

            for data in city_and_date:
                find_city = data.find('h2', class_='new-city_title').text.rstrip()
                city = find_city.split(' ')[1]
                # print(city)

                find_date = data.find('p', class_='new-city-block-title new-city_data').text
                get_date = re.findall('\d+.\d+.\d+', find_date)
                date = str(get_date).replace("'", '').replace('[', '').replace(']', '')
                # print(date)

                link = 'mgresources.ru'
                info = {'product': product, 'price': price, 'city': city, 'date': date, 'link': link}
                write_in_sql(info)


def main():
    url = 'https://mgresources.ru/price/'

    parser_html(get_html(url))


if __name__ == '__main__':
    main()
