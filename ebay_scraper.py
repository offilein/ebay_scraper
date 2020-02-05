import requests
from bs4 import BeautifulSoup


def get_page(url):
    response = requests.get(url)

    if not response.ok:
        print('Server responded:', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup
    

def get_detail_data(soup):
    try:
        t = soup.find('h1', id='itemTitle').text.strip()
        details_zu, title = t.split('\xa0')
    except:
        title = ''

    try:
        p = soup.find('span', id = 'prcIsum').text.strip()
        currency, price = p.split(' ')
    except:
        currency = ''
        price = ''
    
    try:
        sold = soup.find('span',
        class_='vi-qtyS-hot-red').find('a').text.strip().split(' ')[0]
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
        links = soup.find_all('a', class_='s-item_link')
    except:
        links = []

    urls = [item.get('href') for item in links]

    print(urls)


def main():
    url = 'https://www.ebay.de/sch/i.html?_nkw=uhren&_pgn=1'

    get_index_data(get_page(url))
    #get_page(url)




if __name__ == '__main__':
    main()