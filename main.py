from selenium import webdriver
from bs4 import BeautifulSoup

import time

# ! TheGreatFilter.py =============
# * JavaScript Rendering
# * Handle The Pictures issue
# * exploratory data analysis
# todo: More Tests
# todo: split based 3la \n for divs
# todo: better solution for photos
# todo: Check if news are AI news
# todo: Multiple sources collision

# ! Scraping =============
# todo : Needs Better Selenium Implementation
# todo : Solve The Different Sources Problem
# todo : Always Check for Time

# ! ModelAnalsis.py =============
# todo: Parameters Tuning

# ! =============================

WAITING_TIME = 10  # how much to wait for the page to load

def get_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.page_load_strategy = 'eager' 
    driver = webdriver.Chrome(options=chrome_options) 
    return driver

def fetch_text(url, method=0):
    # Load Target Page
    driver = get_driver()
    driver.get(url)
    time.sleep(WAITING_TIME)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(WAITING_TIME*2)


    #Get Posts
    posts = 

    html = driver.page_source
    driver.quit()
    return html