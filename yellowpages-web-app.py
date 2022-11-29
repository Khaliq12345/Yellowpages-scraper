import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from latest_user_agents import get_random_user_agent
ua = get_random_user_agent()

st.set_page_config(page_title= 'Yellowpages.com Scraper', page_icon=":man:")
hide_menu = """
<style>
#MainMenu {
    visibility:hidden;}
footer {
    visibility:hidden;}
</style>
"""

def scraper1():
    item_list = []
    url = listing_url
    isNext = True
    x = 0
    col1, col2 = st.columns(2)
    progress = col1.metric('Pages scraped', 0)
    while isNext:
        x = x + 1
        headers = {'User-Agent': ua}
        response = requests.get(url, headers=headers)
        progress.metric('Pages scraped', x)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.select('.result')
        try:
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
        except:
            pass
        try:
            n_page = soup.select_one('.next.ajax-page')['href']
            url = 'https://www.yellowpages.com' + n_page
        except:
            isNext = False
            break

    df = pd.DataFrame(item_list)
    col2.metric('Total data scrape', len(df))
    st.dataframe(df)

    csv = df.to_csv().encode('utf-8')
    st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='yellowpages-data.csv',
    mime='text/csv',
    )

def scraper2():
    item_list = []
    y = 0
    col1, col2 = st.columns(2)
    progress = col1.metric('Pages scraped', 0)
    for x in range(1, int(pages)):
        y = y + 1
        headers = {'User-Agent': ua}
        response = requests.get(f'https://www.yellowpages.com/search?search_terms={category}&geo_location_terms={location}&page={x}' ,headers=headers)
        progress.metric('Pages scraped', y)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.select('.result')
        try:
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
        except:
            pass
    df = pd.DataFrame(item_list)
    col2.metric('Total data scrape', len(df))
    st.dataframe(df)

    csv = df.to_csv().encode('utf-8')
    st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='yellowpages-data.csv',
    mime='text/csv',
    )



if __name__ == '__main__':
    st.title('YELLOWPAGES.COM SCRAPER')
    st.caption('Field to be scraped are: Name, website, Phone, Address, Reviews count')
    tab1, tab2 = st.tabs(['Scraping with url', 'Scraping with parameters'])

    with tab1.form('Scraper with listing url'):
        listing_url = st.text_input('Paste a listing url')
        start1 = st.form_submit_button('Scrape!')
    if start1:
        scraper1()
        st.balloons()
        st.success('Done!')

    with tab2.form('Scraper with parameters'):
        category = st.text_input('Keyword EX: Restaurants')
        location = st.text_input('Location EX: Miami, Florida')
        pages = st.number_input('Number of pages to scrape')
        start2 = st.form_submit_button('Scrape!')
    if start2:
        scraper2()
        st.balloons()
        st.success('Done!')




