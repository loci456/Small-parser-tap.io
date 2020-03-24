from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests
import os
import re
from random import choice
from multiprocessing import Pool

page = []  
URL = 'https://www.tap.io/app/{}'  


def get_proxy():  
    html = requests.get('https://free-proxy-list.net/').text 
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', id='proxylisttable').find_all('tr')[1:11]  
   

    proxies = []

    for tr in trs: 
        tds = tr.find_all('td')
        ip = tds[0].text.strip()
        port = tds[1].text.strip()
        schema = 'https' if 'yes' in tds[6].text.strip() else 'http'
        proxy = {'schema': schema, 'address': ip + ':' + port}
        proxies.append(proxy)
    return choice(proxies)


def ge(url):
    p = get_proxy() 
    proxy = {p['schema']: p['address']}  
    print(proxy)
    print(url)
    try:
        urlopen(url)
        get = requests.get(url, proxies=proxy)  
        soup = BeautifulSoup(get.text, 'lxml')  
        title = soup.find('span', class_='flex-text title-text').get_text()  
        developer = soup.find('span', itemprop="name").get_text() 
        description = soup.find('div', id='description').get_text()  
        image = soup.find('img', itemprop="image")['src']  

        if os.path.exists(title):
            print('Folder exist')
            pass

        else:  
            clear_str = re.sub(r'[^\w\s]', '', title)  
            os.mkdir(clear_str)

            with open(os.path.join(clear_str, clear_str + '.txt'), 'a', encoding='utf-8') as file:
                file.write('title: ' + title + '\n' + 'developer: ' + developer + '\n' + 'description: ' + description)  
                file.close()

            with open(os.path.join(clear_str, clear_str + '.jpg'),'wb') as load:
                u = requests.get(image)
                load.write(u.content)
                load.close()

        print(developer + '\n' + title + '\n' + description + '\n' + image)

    except HTTPError as e:

        if e.code == 404:  
            print('Page not found')  

        else:  
            print('some else error')  


def main(): 
    ur = URL 
    urls = [ur.format(str(i)) for i in range(1, 999999)] # The number 999999 is responsible for the search range.
    with Pool(20) as p:  # Number 20 - number of processes
        p.map(ge, urls)


if __name__ == '__main__':
    main()
