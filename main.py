from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import math

from TheGreatFilter import filter_html

import json

import time
from datetime import datetime, timedelta
import dateparser

# ! TheGreatFilter.py ===========
# * JavaScript Rendering
# * Handle The Pictures issue
# * exploratory data analysis
# todo: split based 3la \n for divs
# todo: better solution for photos
# todo: Multiple sources collision

# ! TheNexus.py ===========
# todo: Check if news are AI news
# todo: include Time + Source
# todo: Check for duplicates

# ! Scraping ====================
# * Needs Better Selenium Implementation
# * Solve The Different Sources Problem
# * Always Check for Time
# todo: Pop-up ads
# todo: Bypass CDN

# ! ModelAnalsis.py =============
# todo: Parameters Tuning

# ! Additional Tasks ============
# todo: Explaining Basic Concepts
# todo: Logging system 
# todo: parallel execution

# ! Testing =====================
# todo: Testing System to check for accuracy
# todo: CI implementation

# ! =============================



# > ============ Constants ======================
WAITING_TIME = 4        # how much to wait for the page to load
THRESHOLD = 8           # Days for news to be considered recent
EPS = 1.2               # dkshi dyal dbscan
MIN_SAMPLES = 8         # dkshi dyal dbscan
SCROLL = 5              # number of times to scroll
IS_SIMILAR = 0.6        # percentage of characters that should be same for 2 posts to be considered equal
# > =============================================



# Load Web Driver
def get_driver():
    chrome_options = uc.ChromeOptions()
    # chrome_options.add_argument("--headless=new")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    chrome_options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
    chrome_options.page_load_strategy = 'eager' 
    driver = uc.Chrome(options=chrome_options) 
    return driver

def scroll_and_wait(driver, scroll_times, wait_time):
    time.sleep(wait_time)


# Check for recent news
def is_recent(date,threshold):
    current_date = datetime.now()
    day_limit = current_date - timedelta(days=threshold)
    post_date = dateparser.parse(date)
    return post_date >= day_limit

# Retrieve news from each post and feed it to The Grea(t Filter
def get_news_from_post(index, Source, driver):

    # Go To Posts Page
    query = Source["post"] + (f" {Source["click"]}" if Source["click"] != "<self>" else "")
    driver.execute_script("window.history.pushState({}, '', document.URL);")
    driver.execute_script(f"document.querySelectorAll('{ query }')[{ index }].click();")
    time.sleep(WAITING_TIME)
    html = driver.page_source

    # The Great Filter in action
    pure_news = filter_html(html, EPS, MIN_SAMPLES)

    # Close Tab if new one is created, go back if none is created
    tabs = driver.window_handles
    if (len(tabs) > 1):
        driver.switch_to.window(tabs[-1]) 
        driver.close()
        driver.switch_to.window(tabs[0])
    else :
        driver.back()
        time.sleep(WAITING_TIME)

    return pure_news

def get_available_posts(html, Source, driver, history):
    soup = BeautifulSoup(html, "html.parser")
    posts = soup.select(Source["post"])

    # Finding recent posts
    for i, post in enumerate(posts):
        comparing_length = math.floor(len(post.get_text().strip()) * IS_SIMILAR)
        if (post.get_text().strip()[:comparing_length] in history):
            continue
        if (post.select_one(Source["time"])):
            post_time = post.select_one(Source["time"])
            if (is_recent(post_time.get_text().strip(), THRESHOLD)):
                history.append(post.get_text().strip()[:comparing_length] )
                print(str(len(history)) + " | " + post.get_text(separator=" ").strip())
                pure_news = get_news_from_post(i,Source, driver)

                # Save Found News to a file
                name = Source["source"] + " Post " + str(len(history))
                with open(f"./ExtractedNews/{ name }.txt", "w") as f:
                    f.write(driver.current_url + "\n" + "\n".join(pure_news))

        else : 
            print(f"Post doesn't contain expected time : {post_time}")


# Get Recent News
def main():

    # Load Sources from file
    with open("Sources.json") as f:
        Sources = json.loads(f.read())
    
    # Iterate through the sources
    driver = get_driver()
    for Source in Sources:
        history = []
        print("="*50)
        driver.get(Source["url"])

        # scroll and wait for posts to load
        for i in range(SCROLL):
            time.sleep(WAITING_TIME)
            html = driver.page_source
            get_available_posts(html, Source, driver, history)
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
             

    driver.quit()


main()