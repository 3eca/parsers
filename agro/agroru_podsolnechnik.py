import csv
import re
import requests
from bs4 import BeautifulSoup
import pymysql

headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application'
                     '/signed-exchange;v=b3;q=0.9',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.'
                         '3945.130 Safari/537.36'}

ads_urls_list_buy = []
ads_urls_list_sell = []


def get_html(url, headers):
    r = requests.get(url, headers=headers)
    return r.text


# def write_csv(data):
#     name_file = 'agroru_podsolnechnik.csv'
#     with open(name_file, 'a', errors='ignore', newline='') as file:
#         writer = csv.writer(file, delimiter=';')
#         writer.writerow((data['product'], data['price'], data['city'], data['date']))


def write_in_sql(data):
    connect = pymysql.connect(host='localhost', user='', password='', db='', charset='utf8')
    cursor = connect.cursor()
    write_sql = '''INSERT INTO Podsolnechnik (Ad, Price, Region, Date) VALUES ('%s', '%s', '%s', '%s', '%s')''' % \
                (data['product'], data['price'], data['city'], data['date'], data['link'])
    cursor.execute(write_sql)
    connect.commit()
    connect.close()


def get_total_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    last_page_url = soup.find_all('span', class_='regular')[-1].text
    return int(last_page_url) + 1


def get_urls_ads_buy(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls_ads = soup.find_all('div', class_='dl_item')

    for urls in urls_ads:
        url = urls.find('div', class_='dl_t_hdr').find('a').get('href')
        ads_urls_list_buy.append('https://agroru.com' + str(url))

    urls_ads_2 = soup.find_all('div', class_='dl_item sel')

    for urls in urls_ads_2:
        url = urls.find('div', class_='dl_t_hdr').find('a').get('href')
        ads_urls_list_buy.append('https://agroru.com' + str(url))


def get_urls_ads_sell(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls_ads = soup.find_all('div', class_='dl_item')

    for urls in urls_ads:
        url = urls.find('div', class_='dl_t_hdr').find('a').get('href')
        ads_urls_list_sell.append('https://agroru.com' + str(url))

    urls_ads_2 = soup.find_all('div', class_='dl_item sel')

    for urls in urls_ads_2:
        url = urls.find('div', class_='dl_t_hdr').find('a').get('href')
        ads_urls_list_sell.append('https://agroru.com' + str(url))


def parser_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    ads = soup.find_all('div', class_='dd_cont')
    links = soup.find_all('div', class_='top_auth guest')

    for ad in ads:
        try:
            price = ad.find('div', style='white-space:nowrap;').find('span', class_='dd_price').text
            # print(price)
        except:
            price = ''
        if len(price) < 8:
            continue
        if price != '':
            try:
                if len(price) == 8:
                    delete_virgule = price.replace(',', '.').split()
                    price = delete_virgule[0] + str('руб/кг')
                    # print(price)
            except:
                continue
            try:
                if len(price) > 8:
                    delete_virgule = price.replace(',', '').split()
                    restore_price = delete_virgule[0] + delete_virgule[1]
                    get_digits = float(int(restore_price) / 100000)
                    price = '%.02fруб/кг' % get_digits
                    # print(price)
            except:
                continue

            message = ad.find('p', class_='dd_text').text
            lower = message.lower()
            find_tovar = re.compile('(подсолнечник)')
            if re.search(find_tovar, lower) is not None:
                # print(find_tovar)
                product = 'Подсолнечник'
                # print(tovar)

                try:
                    city = ad.find('div', style='overflow: hidden;margin-bottom:10px;').text
                    # print(city)
                except:
                    continue

                try:
                    dates = ad.find('p', class_='dd_date').text.split()[2]
                    get_date = dates.replace('-', '.')
                    date = get_date
                    if len(dates) < 9:
                        date = ''
                    # print(date)
                except:
                    continue

                for i in links:
                    find_link = i.find('a').find_next('a').get('href').split('=')[2]
                    link = 'https://agroru.com' + str(find_link)
                    # print(link)

                    info = {'price': price, 'product': product, 'city': city, 'date': date, 'link': link}
                    # write_csv(info)
                    write_in_sql(info)


def soya_sell():
    url = 'https://agroru.com/doska/semena-maslichnykh-kultur/ct-0-p1.htm'
    base_part_url = 'https://agroru.com/doska/semena-maslichnykh-kultur/ct-0-p'
    end_part_url = '.htm'
    total_pages = get_total_pages(get_html(url, headers))
    for i in range(1, total_pages):
        url_generation = base_part_url + str(i) + end_part_url
        html = get_html(url_generation, headers)
        get_urls_ads_buy(html)

    count = 0
    ads_urls_set_buy = set(ads_urls_list_buy)
    for urls in ads_urls_set_buy:
        count += 1
        parser_html(get_html(urls, headers))
        # print('Parsing url buy %d%%' % (count / len(ads_urls_set_buy) * 100))
    # url = 'https://agroru.com/spros/soya-boby-65100.htm'
    # parser_html(get_html(url, headers))


def main():
    soya_sell()


if __name__ == '__main__':
    main()
