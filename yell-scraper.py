from time import sleep
from playwright.sync_api import sync_playwright
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from latest_user_agents import get_random_user_agent
ua = get_random_user_agent()


def scrape():
    items_list = []
    pages = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(user_agent = ua)
        isNext = True
        url = 'https://www.yell.com/ucs/UcsSearchAction.do?keywords=Plumbers&location=New+York&scrambleSeed=1358346792'
        while isNext:
            pages = pages + 1
            page.goto(url)
            print(f"Page {pages}")
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

    print(pd.DataFrame(items_list))


scrape()
