from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import re
import pymysql

ads_city_dict = {'Таганрог': ['CPT ТСРЗ'],
                 'Туапсе': ['CPT Туапсе'],
                 'Новороссийск': ['CPT НЗТ', 'CPT КСК']
                 }


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
    global price, product
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find_all('div', class_='p1-box_sm_table')
    dates = soup.find('h5', style='margin-top: 20px; text-align: center;')

    for ad in ads:
        search_citys = ad.find('table', class_='p1-table_small').find_all('th')
        search_datas = ad.find('table', class_='p1-table_small').find_all('td')

        for search_data in search_datas:
            find_price = search_data.text
            find_product = search_data.text.lower()

            if re.match('пшеница.\d.\w+', find_product):
                product = re.split('\s\s', find_product)[0]

            if re.match('\d+\s\d+', find_price):
                format_price = re.sub('\W', '', find_price)
                price = '%0.2f' % float(int(format_price) / 1000) + 'руб/кг.'
                find_date = dates.text.rstrip().lstrip()
                get_date = str(re.findall('\d+.\d+.\d+', find_date))
                date = get_date.replace('[', '').replace(']', '').replace("'", '')

                for search_city in search_citys:
                    find_city = search_city.text
                    for key, value in ads_city_dict.items():
                        if find_city in value:
                            city = key
                            link = 'zerno-trade.biz'

                            info = {'product': product, 'price': price, 'city': city, 'date': date, 'link': link}
                            write_in_sql(info)

        search_citys = ad.find('table', class_='p1-table_small').find_next('table', class_='p1-table_small').find_all(
            'th')
        search_datas = ad.find('table', class_='p1-table_small').find_next('table', class_='p1-table_small').find_all(
            'td')

        for search_data in search_datas:
            find_price = search_data.text
            find_product = search_data.text.lower()

            if re.match('пшеница.\d.\w+', find_product):
                product = re.split('\s\s', find_product)[0]

            if re.match('\d+\s\d+', find_price):
                format_price = re.sub('\W', '', find_price)
                price = '%0.2f' % float(int(format_price) / 1000) + 'руб/кг.'
                find_date = dates.text.rstrip().lstrip()
                get_date = str(re.findall('\d+.\d+.\d+', find_date))
                date = get_date.replace('[', '').replace(']', '').replace("'", '')

                for search_city in search_citys:
                    find_city = search_city.text
                    for key, value in ads_city_dict.items():
                        if find_city in value:
                            city = key
                            link = 'zerno-trade.biz'

                            info = {'product': product, 'price': price, 'city': city, 'date': date, 'link': link}
                            write_in_sql(info)

        search_citys = ad.find('table', class_='p1-table_small').find_next('table', class_='p1-table_small').find_next(
            'table', class_='p1-table_small').find_all('th')
        search_datas = ad.find('table', class_='p1-table_small').find_next('table', class_='p1-table_small').find_next(
            'table', class_='p1-table_small').find_all('td')

        for search_data in search_datas:
            find_price = search_data.text
            find_product = search_data.text.lower()

            if re.match('пшеница.\d.\w+', find_product):
                product = re.split('\s\s', find_product)[0]

            if re.match('\d+\s\d+', find_price):
                format_price = re.sub('\W', '', find_price)
                price = '%0.2f' % float(int(format_price) / 1000) + 'руб/кг.'
                find_date = dates.text.rstrip().lstrip()
                get_date = str(re.findall('\d+.\d+.\d+', find_date))
                date = get_date.replace('[', '').replace(']', '').replace("'", '')

                for search_city in search_citys:
                    find_city = search_city.text
                    for key, value in ads_city_dict.items():
                        if find_city in value:
                            city = key
                            link = 'zerno-trade.biz'

                            info = {'product': product, 'price': price, 'city': city, 'date': date, 'link': link}
                            write_in_sql(info)

        search_citys = ad.find('table', class_='p1-table_small').find_next('table', class_='p1-table_small').find_next(
            'table', class_='p1-table_small').find_next(
            'table', class_='p1-table_small').find_all('th')
        search_datas = ad.find('table', class_='p1-table_small').find_next('table', class_='p1-table_small').find_next(
            'table', class_='p1-table_small').find_next(
            'table', class_='p1-table_small').find_all('td')

        for search_data in search_datas:
            find_price = search_data.text
            find_product = search_data.text.lower()

            if re.match('пшеница.\d.\w+', find_product):
                product = re.split('\s\s', find_product)[0]

            if re.match('\d+\s\d+', find_price):
                format_price = re.sub('\W', '', find_price)
                price = '%0.2f' % float(int(format_price) / 1000) + 'руб/кг.'
                find_date = dates.text.rstrip().lstrip()
                get_date = str(re.findall('\d+.\d+.\d+', find_date))
                date = get_date.replace('[', '').replace(']', '').replace("'", '')

                for search_city in search_citys:
                    find_city = search_city.text
                    for key, value in ads_city_dict.items():
                        if find_city in value:
                            city = key
                            link = 'zerno-trade.biz'

                            info = {'product': product, 'price': price, 'city': city, 'date': date, 'link': link}
                            write_in_sql(info)


def main():
    url = 'https://zerno-trade.biz/'
    parser_html(get_html(url))


if __name__ == '__main__':
    main()
