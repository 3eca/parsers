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


def get_html(url, headers):
    r = requests.get(url, headers=headers, verify=False)
    return r.text


# def write_csv(data):
#     name_file = 'rif.csv'
#     with open(name_file, 'a', errors='ignore', newline='') as file:
#         writer = csv.writer(file, delimiter=';')
#         writer.writerow((data['product'], data['price'], data['city'], data['date']))

def write_in_sql(data):
    connect = pymysql.connect(host='localhost', user='', password='', db='', charset='utf8')
    cursor = connect.cursor()
    write_sql = '''INSERT INTO Podsolnechnik (Ad, Price, Region, Date) VALUES ('%s', '%s', '%s', '%s')''' % \
                (data['product'], data['price'], data['city'], data['date'])
    cursor.execute(write_sql)
    connect.commit()
    connect.close()


def parser_html(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find_all('div', class_='main-price-elevator-item')
    for ad in ads:
        find_all_price = ad.find('table', class_='price').find_all('tr', class_='line-second price-data')
        # print(find_all_price)
        for find_price in find_all_price:
            get_price = find_price.find('td').text.rstrip().lstrip().replace(',', '.').replace('р.', 'руб/кг')
            search_digits = re.search('(\d+.\d+)', get_price)
            if search_digits is not None:
                price = get_price
                # print(price)

                get_product = ad.find('div', class_='name').text.lower().rstrip().lstrip()
                search_product = re.search('(подсолнечник)', get_product)
                if search_product is not None:
                    product = get_product
                    # print(product)

                    find_region = ad.find('p').text
                    search_city = re.search('(г.\s\w+)', find_region)
                    if search_city is not None:
                        city = search_city.group().split()[1]
                        # print(city)

                        find_date = ad.find('h3').find('span').text.split()[0]
                        date = datetime.strptime(find_date, '%d.%m.%Y').strftime('%d.%m.%y')
                        # print(date)

                        info = {'product': product, 'price': price, 'city': city, 'date': date}
                        write_in_sql(info)
                        # print(info)


def main():
    url = 'https://rif-rostov.ru/price/?arElevators%5B%5D=231&arElevators%5B%5D=99754&arElevators%5B%5D=42711' \
          '&arElevators%5B%5D=42639&arElevators%5B%5D=99417&arElevators%5B%5D=99738&arElevators%5B%5D=42643' \
          '&arElevators%5B%5D=42647&arElevators%5B%5D=99418&arElevators%5B%5D=96279&arElevators%5B%5D=97237' \
          '&arElevators%5B%5D=96465&arElevators%5B%5D=226&arElevators%5B%5D=227&arElevators%5B%5D=98900&arElevators' \
          '%5B%5D=576&arElevators%5B%5D=96517&arElevators%5B%5D=233&arElevators%5B%5D=97268&arCrops%5B%5D=131 '

    parser_html(get_html(url, headers))


if __name__ == '__main__':
    main()
