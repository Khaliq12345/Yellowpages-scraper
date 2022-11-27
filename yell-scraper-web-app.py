import os
os.system("playwright install chromium")
import streamlit as st
from playwright.sync_api import sync_playwright
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from latest_user_agents import get_random_user_agent
ua = get_random_user_agent()

def scrape2():
    items_list = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent= ua)
        col1, col2 = st.columns(2)
        progress = col1.metric('Pages scraped', 0)
        x = 0
        isNext = True
        url = f"https://www.yell.com/ucs/UcsSearchAction.do?keywords={keyword}&location={city},{state}"
        while isNext:
            x = x + 1
            page.goto(url)
            progress.metric('Pages scraped', x)
            try:
                page.wait_for_selector('.businessCapsule--mainRow')
                html = page.inner_html('#rightNav')
                soup = BeautifulSoup(html, 'html.parser')
                cards = soup.select('.businessCapsule--mainRow')
                for card in cards:
                    try:
                        name = card.select_one('.text-h2').text
                    except:
                        name = None
                    try:
                        website = card.select_one('a.businessCapsule--ctaItem')['href']
                    except:
                        website = None
                    try:
                        phone = card.select_one('.business--telephoneNumber').text
                    except:
                        phone = None
                    try:
                        address = card.select_one('.businessCapsule--link').text.split('|')
                        address = address[1]
                    except:
                        address = None
                    try:
                        about = card.select_one('.businessCapsule--classStrap').text
                    except:
                        about = None
                    try:
                        rate = card.select_one('.starRating--average').text
                    except:
                        rate = None
                    try:
                        reviews = card.select_one('.starRating--total span').text  
                    except:
                        reviews = None
                    
                    items = {
                        'Name': name,
                        'Website': website,
                        'Phone': phone,
                        'Address': address,
                        'About': about,
                        'Rating': rate,
                        'Total reviews': reviews
                    }
                    items_list.append(items)
            except:
                pass
                print('Parameter error! Try scraping by link')

            try:
                page.locator('.pagination--next').click()
                url = 'https://www.yell.com' + soup.select_one('.pagination--next')['href']
                sleep(2)
            except:
                isNext = False
                break
                
        browser.close()

    df = pd.DataFrame(items_list)
    col2.metric('Total data scrape', len(df))
    st.dataframe(df)

    csv = df.to_csv().encode('utf-8')
    st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name=f'yell-{keyword}-data.csv',
    mime='text/csv',
    )

def scrape1():
    items_list = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent = ua)
        col1, col2 = st.columns(2)
        progress = col1.metric('Pages scraped', 0)
        x = 0
        isNext = True
        url = yell_url
        while isNext:
            x = x + 1
            page.goto(url)
            progress.metric('Pages scraped', x)
            page.wait_for_selector('.businessCapsule--mainRow')
            html = page.inner_html('#rightNav')
            soup = BeautifulSoup(html, 'html.parser')
            cards = soup.select('.businessCapsule--mainRow')
            for card in cards:
                try:
                    name = card.select_one('.text-h2').text
                except:
                    name = None
                try:
                    website = card.select_one(
                        'a.businessCapsule--ctaItem')['href']
                except:
                    website = None
                try:
                    phone = card.select_one('.business--telephoneNumber').text
                except:
                    phone = None
                try:
                    address = card.select_one(
                        '.businessCapsule--link').text.split('|')
                    address = address[1]
                except:
                    address = None
                try:
                    about = card.select_one(
                        '.businessCapsule--classStrap').text
                except:
                    about = None
                try:
                    rate = card.select_one('.starRating--average').text
                except:
                    rate = None
                try:
                    reviews = card.select_one('.starRating--total span').text
                except:
                    reviews = None

                items = {
                    'Name': name,
                    'Website': website,
                    'Phone': phone,
                    'Address': address,
                    'About': about,
                    'Rating': rate,
                    'Total reviews': reviews
                }
                items_list.append(items)
            try:
                url = 'https://www.yell.com' + soup.select_one('.pagination--next')['href']
                sleep(2)
            except:
                isNext = False
                break

        browser.close()
    df = pd.DataFrame(items_list)
    col2.metric('Total data scrape', len(df))
    st.dataframe(df)

    csv = df.to_csv().encode('utf-8')
    st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name=f'yell-{keyword}-data.csv',
    mime='text/csv',
    )
        
if __name__ == '__main__':
    st.title('YELL.COM SCRAPER')
    st.markdown('NB: Scraping with url gives a much more accurate data')
    tab1, tab2 = st.tabs(['Scraping with url', 'Scraping with parameters'])

    with tab1.form('Scraper with listing url'):
        yell_url = st.text_input('Input a listing url')
        start1 = st.form_submit_button('Scrape!')
    if start1:
        scrape1()
        st.balloons()
        st.success('Done!')

    with tab2.form('Scraper with parameters'):
        keyword = st.text_input('Keyword')
        city = st.text_input('City')
        state = st.text_input('State')
        start2 = st.form_submit_button('Scrape!')
    if start2:
        scrape2()
        st.balloons()
        st.success('Done!')


    # if start:
    #     scrape()
    #     st.balloons()
    #     st.success('Done!')


