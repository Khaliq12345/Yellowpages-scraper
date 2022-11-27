from time import sleep
import requests
import pandas as pd
from bs4 import BeautifulSoup
from latest_user_agents import get_random_user_agent
ua = get_random_user_agent()

category = input('Catgeory')
Location = input('Location')

def scrape():
    item_list = []
    url = 'https://www.yellowpages.com/search?search_terms=attorneys&geo_location_terms=Los%20Angeles&page=90'
    isNext = True
    x = 0
    while isNext:
        x = x + 1
        headers = {'User-Agent': ua}
        response = requests.get(url, headers=headers)
        print(f'Page {x}')
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.select('.result')

        for card in cards:
            try:
                name = card.select_one('.business-name').text
            except:
                name = None
            try:
                link = card.select_one('.links a')['href']
            except:
                link = None
            try:
                phone = card.select_one('.phone').text
            except:
                phone = None
            try:
                address1 = card.select_one('.street-address').text
            except:
                address1 = None
            try:
                address2 = card.select_one('.locality').text
            except:
                address2 = None
            try:
                reviews = card.select_one('.count').text.replace(')', '').replace('(', '')
            except:
                reviews = None
            items = {
                'Name': name,
                'Website/social': link,
                'Phone': phone,
                'Address 1': address1,
                'Address 2': address2,
                'Reviews': reviews
            }
            item_list.append(items)

        try:
            n_page = soup.select_one('.next.ajax-page')['href']
            url = 'https://www.yellowpages.com' + n_page
        except:
            isNext = False
            break

    df = pd.DataFrame(item_list)
    print(df)

scrape()