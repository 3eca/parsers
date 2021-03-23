from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import re
import pymysql


ads_city_dict = {'Азов': ['ООО "Ростовская Нива" (Азов)', 'ООО «АТП №9».Российская Федерация, Ростовская область, '
                                                          'г. Азов, ул. Промышленная, д4',
                          'ООО "Азовская перевалочная база", 346780 Ростовская обл., г. Азов, ул. Элеваторная 3',
                          'Азовский портовый элеватор'],
                 'Темрюк': ['Темрюк'],
                 'Ейск': ['АО "Ейский портовый элеватор"'],
                 'Ростов-на-Дону': ['ООО "Гринввуд" (Ростов)', 'ООО "Эльдако Юг" (Ростов)']
                 }


def get_html(url):
    r = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    return r.text


def write_in_sql(data):
    connect = pymysql.connect(host='localhost', user='', password='', db='', charset='utf8')
    cursor = connect.cursor()
    write_sql = '''INSERT INTO Len (Ad, Price, Region, Date, Link) VALUES ('%s', '%s', '%s', '%s', '%s')''' % \
                (data['product'], data['price'], data['city'], data['date'], data['link'])
    cursor.execute(write_sql)
    connect.commit()
    connect.close()


def parser_html(html):
    global city
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('table', class_='table').find('tbody').find_all('tr')
    ads_date = soup.find('h2', style='float:left; margin:20px 20px 0 15px')

    for ad in ads:
        find_price = ad.find('td', style='border-left: 1px dashed rgb(221,221,221); '
                                         'text-align:center;vertical-align:middle;').text.rstrip().lstrip()

        if find_price.isdigit():
            get_price = float(int(find_price) / 1000)
            price = '%0.2f' % get_price + 'руб/кг.'

            find_city = ad.find_previous('th', rowspan="2", style="vertical-align:middle; ").text.rstrip().lstrip()
            get_city = re.split('\r', find_city)

            for key, value in ads_city_dict.items():
                if get_city[0] in value:
                    city = key

            product = 'лён'

            find_date = ads_date.text
            get_date = str(re.findall('\d+.\d+.\d+', find_date))
            if get_date is not None:
                date = get_date[2:-2]

                link = 'sr-company.org'
                info = {'product': product, 'price': price, 'city': city, 'date': date, 'link': link}
                write_in_sql(info)


def main():
    url = 'https://www.sr-company.org/Home/Price?grainTypeFilterId=9'
    parser_html(get_html(url))


if __name__ == '__main__':
    main()
