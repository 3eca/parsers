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
    write_sql = '''INSERT INTO Pshenitsa (Ad, Price, Region, Date) VALUES ('%s', '%s', '%s', '%s')''' % \
                (data['product'], data['price'], data['city'], data['date'])
    cursor.execute(write_sql)
    connect.commit()
    connect.close()


def parser_html(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('table', class_='border').find_all('tr')
    sda = soup.find_all('table', class_='border')
    # print(ads)
    for ad in ads:
        try:
            find_price = ad.find('td', style='background-color:#ffffff; text-align:center;').text.replace(' ', '')
            get_price = float(int(find_price) / 1000)
            price = '%0.2f' % get_price + 'руб/кг.'
            # print(price)
        except:
            continue

        find_product = ad.find('td', style='background-color:#ffffff').text.lower()
        get_product = str(re.findall('(пшеница.\d.\w+)', find_product))
        if get_product is not None:
            product = re.sub('\W+', ' ', get_product).lstrip().rstrip()
            # print(product)

            for da in sda:
                find_city_date = da.find('td', style='background-color:#fbfce3; text-align:center;').find('strong').text.split()
                city = find_city_date[3].replace(',', '').split('.')[1]
                # print(city)
                date = find_city_date[-1]
                # print(date)

                info = {'product': product, 'price': price, 'city': city, 'date': date}
                # print(info)
                write_in_sql(info)
                


def main():
    url = 'http://www.bunge.ru/business/price/'
    parser_html(get_html(url))


if __name__ == '__main__':
    main()
