import requests
from bs4 import BeautifulSoup
import time
import csv

headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application'
                     '/signed-exchange;v=b3;q=0.9',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.'
                         '3945.130 Safari/537.36'
           }

start_time = time.time()


def get_html(url, headers):
    session = requests.session()
    r = requests.get(url, headers=headers)
    return r.text


def write_csv(data):
    with open('key-lol.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for btc in data['btc']:
            if btc != '0':
                writer.writerow((data['btc'],
                                data['private_k'],
                                data['public_k'],
                                data['c_public_k']))
    # with open('key-lol-urls.csv', 'a', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow((data_u['url']))
    # with open('key-lol-all.csv', 'a', newline='') as file:
    #     writer = csv.writer(file, delimiter=';')
    #     writer.writerow((data['balance'],
    #                     data['private_k'],
    #                     data['public_k'],
    #                     data['c_public_k']))


def parser_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    keys_all = soup.find('div', class_='container mx-auto px-2 flex-1').find('div',
                                                                             class_='sm:flex justify-center').find(
        'div', class_='mx-auto').find_all('div',
                                          class_='wallet loading flex flex-col lg:flex-row font-mono text-sm pl-2')

    for keys in keys_all:
        try:
            # получаем баланс кошелька
            balance = keys.find('span', class_='mr-4 inline-block').find('strong', class_='wallet-balance').text
            btc = balance.split(' ')[0]
            # print(btc)
        except:
            print('1error')
            continue

        try:
            # получаем private key кошелька
            private_k = keys.find('span', class_='lg:mr-4 text-xs sm:text-sm break-words').text
            # print(private_k)
        except:
            print('2error')
            continue

        try:
            # получаем public key кошелька
            public_k = keys.find('span', class_='hidden xl:inline-block').text
            # print(public_k)
        except:
            print('3error')
            continue

        try:
            # полчуаем compressed public key
            c_public_k = keys.find('div', class_='lg:block flex').find_all('span',
                                                                           class_='hidden xl:inline-block')[1].text
            # print(c_public_k)
        except:
            print('4error')
            continue

        data = {'balance': balance,
                'btc': btc,
                'private_k': private_k,
                'public_k': public_k,
                'c_public_k': c_public_k}
        # print(data)
        write_csv(data)


def main():
    url = 'https://keys.lol/bitcoin/'
    pages = 400000

    for page in range(1, pages):
        urls = url + str(page)
        # data_u = {'url': urls}
        # write_csv(data_u)
        print('Parsing in work %d%%' % (page / pages * 100), ', page - ', urls)
        parser_html(get_html(urls, headers))

    end_time = time.time()
    print('Parsing completed in', end_time - start_time)


if __name__ == '__main__':
    main()
