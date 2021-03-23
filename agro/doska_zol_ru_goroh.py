import csv
import re
import requests
from bs4 import BeautifulSoup
import pymysql

headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application'
                     '/signed-exchange;v=b3;q=0.9',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.'
                         '3945.130 Safari/537.36'}
ads_urls_list = []


def get_html(url, headers):
    r = requests.get(url, headers=headers)
    return r.text


# def write_csv(data):
#     name_file = 'doska_zol_ru_goroh.csv'
#     with open(name_file, 'a', errors='ignore', newline='') as file:
#         writer = csv.writer(file, delimiter=';')
#         writer.writerow((data['product'], data['price'], data['city'], data['date'], data['link']))


def write_in_sql(data):
    connect = pymysql.connect(host='localhost', user='', password='', db='', charset='utf8')
    cursor = connect.cursor()
    write_sql = '''INSERT INTO Goroh (Ad, Price, Region, Date) VALUES ('%s', '%s', '%s', '%s', '%s')''' % \
                (data['product'], data['price'], data['city'], data['date'], data['link'])
    cursor.execute(write_sql)
    connect.commit()
    connect.close()


def get_urls_ads(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls_ads = soup.find_all('tr', class_='offer_row')

    for url_ad in urls_ads:
        url = url_ad.find('table', class_='smd-content').find('a').get('href')
        ads_urls_list.append(url)


def parser_html(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find_all('div', class_='col-12 news-body')
    ads_data = soup.find_all('div', class_='row mt-3')
    links = soup.find_all('p', align='left')

    for ad in ads:
        try:
            price = ad.find('div', class_='one-price').find('span').text
            # print(price, len(price))
        except:
            price = ''
        if price != '':
            find_rub_tonna = re.search('(руб./т.)', price)
            if find_rub_tonna is not None:
                get_only_digits = str(re.findall('\d+', price)).replace("'", '').replace('[', '').replace(']',
                                                                                                          '').replace(
                    ',', '').replace(' ', '')
                get_digits = float(int(get_only_digits) / 1000)
                price = '%.02fруб/кг' % get_digits

            find_rub_kg = re.search('(руб./кг.)', price)
            if find_rub_kg is not None:
                get_only_digits = str(re.findall('\d+', price)).replace("'", '').replace('[', '').replace(']',
                                                                                                          '').replace(
                    ',', '').replace(' ', '')
                if len(get_only_digits) < 5:
                    price = '%.02fруб/кг' % float(int(get_only_digits))
                    # print(price)

            message = ad.text
            find_product_2 = re.search('(горох)', message)
            if find_product_2 is not None:
                product = 'горох'
                # print(f'Найдено совпадение {find_product_2}')
                for ad_data in ads_data:
                    try:
                        city = ad_data.find('td').find_next('td').text.rstrip().lstrip()
                        # print(city)
                    except AttributeError:
                        continue

                    get_date = ad_data.find('td', colspan='2').find_next('td', colspan='2').find_next('td',
                                                                                                      colspan='2').text
                    get_only_date = get_date.split()[0]
                    date = get_only_date
                    # print(date)

                    for i in links:
                        try:
                            link = i.find_next('p', align='left').find_next('p', align='left').text.split()[2]
                            # print(link)
                        except:
                            continue

                        info = {'price': price, 'product': product, 'city': city, 'date': date, 'link': link}
                        # write_csv(info)
                        write_in_sql(info)


def main():
    base_part_url = 'https://doska.zol.ru/Gorokh/gorokh.html?sell=on&buy=on&nearby_regions=On&without_exact_fo=On&page='
    for i in range(1, 11):
        url_generation = base_part_url + str(i)
        html = get_html(url_generation, headers)
        get_urls_ads(html)

    count = 0
    ads_urls_set = set(ads_urls_list)
    for urls in ads_urls_set:
        count += 1
        parser_html(get_html(urls, headers))
        # print('%d%%' % (count / len(ads_urls_set) * 100))
    # url = 'https://tambov.zol.ru/Pokupka/Gorokh-prodovolstvennyj_Kuplu_gorokh_9818520.html'
    # parser_html(get_html(url, headers))


if __name__ == '__main__':
    main()
