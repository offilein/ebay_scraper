import csv
import requests
from bs4 import BeautifulSoup

#Soup erstellen und prüfen ob Seite erreichbar ist
def get_page(url):
    response = requests.get(url)

    if not response.ok:
        print('Server responded:', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup
    
#Titelö
def get_detail_data(soup):
    try:
        title = soup.find('h1', id='itemTitle').text.strip().replace('Details about   ', '')
    except:
        title = ''

    try:
        try:
            try:
                p = soup.find('span', id = 'mm-saleDscPrc').text.strip()
            except:            
                p = soup.find('span', id = 'prcIsum').text.strip()
        except:
            p = soup.find('span', id='prcIsum_bidPrice').text.strip()
        currency, price = p.split(' ')
    except:
        currency = ''
        price = ''
    
    try:
        sold = soup.find('span',
        class_='vi-qtyS-hot-red').find('a').text.strip().split(' ')[0].replace('\xa0', '')
    except:
        sold = ''

    data = {
        'title': title,
        'price': price,
        'currency': currency,
        'total sold': sold
    }

    return data

def get_index_data(soup):
    try:
        links = soup.find_all('a', class_='s-item__link')
    except:
        links = []

    urls = [item.get('href') for item in links]

    return urls

def write_csv(data, url):
    with open('output.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)

        row = [data['title'], data['price'], data['currency'], data['total sold'], url]

        writer.writerow(row)

def main():
    url = 'https://www.ebay.com/sch/i.html?_nkw=paper+mario+n64&_pgn=1'

    products = get_index_data(get_page(url))

    for link in products:
        data = get_detail_data(get_page(link))
        write_csv(data, link)


if __name__ == '__main__':
    main()
