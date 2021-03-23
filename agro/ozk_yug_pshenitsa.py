from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import re
import pymysql

ads_urls_list = []
city_dict = {'Башкортостан': ['http://ozk-yug.ru/ooo_konsaltsitighrup',
                              'http://ozk-yug.ru/ooo_buzdiakskii_elievator',
                              'http://ozk-yug.ru/ooo_mielieuzovskii_elievator',
                              'http://ozk-yug.ru/ooo_zirghanskii_elievator',
                              'http://ozk-yug.ru/ooo_novatrieid_stallaghuvat'],
             'Ульяновская область': ['http://ozk-yug.ru/ao_novospasskii_elievator'],
             'Самарская область': ['http://ozk-yug.ru/ooo_obsharovskaia_khliebnaia_baza'],
             'Орловская область': ['http://ozk-yug.ru/ooo_tzk_ziernovyie_produkty'],
             'Оренбургская область': ['http://ozk-yug.ru/ao_novosierghiievskii_elievator',
                                      'http://ozk-yug.ru/oao_orskii_elievator'],
             'Саратовская область': ['http://ozk-yug.ru/ooo_pitierskii_khlieb',
                                     'http://ozk-yug.ru/ooo_aghrosnab',
                                     'http://ozk-yug.ru/ooo_kistiendieiskii_elievator',
                                     'http://ozk-yug.ru/ooo_prikhopierskii_elievator',
                                     'http://ozk-yug.ru/ooo_tatishchievskii_kkhp',
                                     'http://ozk-yug.ru/ao_iekatierinovskii_elievator',
                                     'http://ozk-yug.ru/ooo_pughachievkhlieboprodukt',
                                     'http://ozk-yug.ru/oao_balashovskaia_khliebnaia_baza'],
             'Ростовская область': ['http://ozk-yug.ru/ooo_krasnosulinskoie_khpp',
                                    'http://ozk-yug.ru/ooo_elievator_prolietarskii',
                                    'http://ozk-yug.ru/oao_novoshakhtinskkhlieboprodukt'],
             'Пензенская область': ['http://ozk-yug.ru/ao_bashmakovskii_elievator',
                                    'http://ozk-yug.ru/ao_impulsinviest'],
             'Курская область': ['http://ozk-yug.ru/ooo_korporatsiia_kurskaia_khliebnaia_baza_24',
                                 'http://ozk-yug.ru/ooo_khpp_konyshievskii_elievator'],
             'Липецкая область': ['http://ozk-yug.ru/ooo_dobrinskii_elievator',
                                  'http://ozk-yug.ru/ao_izmalkovskii_elievator_rabotnikov_np'],
             'Тамбовская область': ['http://ozk-yug.ru/ao_oktiabrskoie_zhdst_sieliezni_iuvs'],
             'Ставропольский край': ['http://ozk-yug.ru/ao_elievator',
                                     'http://ozk-yug.ru/grachievskii_elievator'],
             'Воронежская область': ['http://ozk-yug.ru/buturlinovskii_mielkombinat',
                                     'http://ozk-yug.ru/ooo_elievator_kommoditi_kolodieznoie',
                                     'http://ozk-yug.ru/ooo_novokhopierskii_khlieb',
                                     'http://ozk-yug.ru/ao_gribanovskoie_khpp'],
             'Волгоградская область': ['http://ozk-yug.ru/surovikinskii_elievator',
                                       'http://ozk-yug.ru/ooo_siebriakovskii_maslozavod',
                                       'http://ozk-yug.ru/oao_novoanninskii_kkhp',
                                       'http://ozk-yug.ru/oao_uriupinskii_elievator',
                                       'http://ozk-yug.ru/ao_viazovskoie_khpp'],
             'Краснодарский край': ['http://ozk-yug.ru/pao_nkkhp',
                                    'http://ozk-yug.ru/ao_rovnenskii_elievator',
                                    'http://ozk-yug.ru/ao_kkhp_tikhorietskii',
                                    'http://ozk-yug.ru/ooo_azt_isladam']
             }


def write_in_sql(data):
    connect = pymysql.connect(host='localhost', user='', password='', db='', charset='utf8')
    cursor = connect.cursor()
    write_sql = '''INSERT INTO Pshenitsa (Ad, Price, Region, Date) VALUES ('%s', '%s', '%s', '%s')''' % \
                (data['product'], data['price'], data['city'], data['date'])
    cursor.execute(write_sql)
    connect.commit()
    connect.close()


def get_html(url):
    r = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    return r.text


def get_ads_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    find_urls = soup.find_all('div', class_='container js-block-container')
    for urls in find_urls:
        try:
            url = urls.find('div', class_='ul-widget ul-w-button text-left').find('a').get('href')
            ads_urls_list.append('http://ozk-yug.ru' + url)
        except:
            continue


def parser_html(html):
    global product, city, date
    soup = BeautifulSoup(html, 'html.parser')
    find_city = soup.find_all('meta', property='og:url')
    ads_body = soup.find_all('div', class_='container js-block-container')
    ads = soup.find('tr', class_='ul-w-table-head').find_all_next('tr')
    for ad in ads:
        find_price = ad.find_next('td').find_next('td').find_next('td').text
        if len(find_price) > 1:
            if find_price.isdigit():
                get_price = float(int(find_price) / 1000)
                price = '%0.2f' % get_price + 'руб/кг.'
                # print(price)

                find_product = ad.find_next('td').text
                lower = find_product.lower()
                get_product = re.findall('(пшеница)', lower)
                if get_product is not None:
                    product = lower
                    # print(product)

                for ads in ads_body:
                    find_date = ads.find('span', attrs={'data-text': 'true'}).find_next('span').text
                    get_date = re.findall('\d+.\d+.\d+', find_date)
                    date = str(get_date).replace('[', '').replace(']', '').replace("'", '')
                    # print(date)

                for get_city in find_city:
                    url = get_city.get('content')
                    for key, val in city_dict.items():
                        if url in val:
                            city = key
                            # print(city)

                info = {'product': product, 'price': price, 'date': date, 'city': city}
                write_in_sql(info)


def main():
    url = 'http://ozk-yug.ru/price'
    get_ads_urls(get_html(url))
    for urls in ads_urls_list:
        parser_html(get_html(urls))


if __name__ == '__main__':
    main()
