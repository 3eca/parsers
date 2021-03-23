from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime
import pymysql


ads_url_list = []


def get_html(url):
    r = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    return r.text


# def write_csv(data):
#     name_file = 'cargill_pshenitsa.csv'
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


def get_urls(html):
    soup = BeautifulSoup(html, 'lxml')
    find_urls = soup.find('div', class_='lvl lvl-4').find_all('li')
    for urls in find_urls:
        get_url = urls.find('a').get('href')
        # print(get_url)
        ads_url_list.append(get_url)


def parser_html(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='content-drop-one').find_all('script')
    for ad in ads:
        try:
            find_csv = str(re.findall('(https?://[^\"\s]+)', str(ad)))
            if len(find_csv) > 4:
                url_csv = find_csv.replace('[', '').replace(']', '').replace('"', '').replace("'", '')
                # print(url_csv)
                r = requests.get(url_csv)
                with open('cargill.csv', 'ab') as f:
                    f.write(r.content)
        except:
            continue


def read_csv():
    with open('cargill.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for line in reader:
            find_city = line[0]
            get_city = re.search('^(?!Пункт)\w+.*', str(find_city))
            if get_city is not None:
                city = find_city.split('.')[-1].split()[-1]
                # print(city)

                find_product = line[1].lower()
                get_product = re.search('^(?!наименование)\w+.*', find_product)
                if get_product is not None:
                    take_product = re.search('(пшеница.\w+.\d.\w+)', find_product)
                    if take_product is not None:
                        product = re.sub('\sпродовольственная', '', find_product)[:16]
                        # print(product)

                        find_price = line[2]
                        get_price = re.search('\d+', find_price)
                        if get_price is not None:
                            take_price = float(int(find_price) / 1000)
                            price = '%0.2f' % take_price + 'руб/кг.'
                            # print(price)

                            date = datetime.strftime(datetime.today(), '%d.%m.%Y')
                            # print(date)

                            info = {'product': product, 'price': price, 'city': city, 'date': date}
                            # print(info)
                            # write_csv(info)
                            write_in_sql(info)


def main():
    url = 'https://www.cargill.ru/ru/%D1%81%D0%B5%D0%BB%D1%8C%D1%81%D0%BA%D0%BE%D0%B5-%D1%85%D0%BE%D0%B7%D1%8F%D0%B9' \
          '%D1%81%D1%82%D0%B2%D0%BE '
    get_urls(get_html(url))
    for link in ads_url_list:
        parser_html(get_html(link))
    read_csv()


if __name__ == '__main__':
    main()
