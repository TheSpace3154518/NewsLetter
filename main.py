from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from concurrent import futures
import traceback

from logs_system import generate_logs

import math

from constants import *
from TheGreatFilter import filter_html

import json

import time
from datetime import datetime, timedelta
import dateparser

# ! TheGreatFilter.py ===========
# * JavaScript Rendering
# * Handle The Pictures issue
# * exploratory data analysis
# * split based 3la \n for divs
# todo: better solution for photos

# ! TheNexus.py ===========
# * Check if news are AI news
# * Multiple sources collision
# * Unsubscribe Button
# todo: include Sources
# todo: Languages

# ! API ===========
# todo: homepage html
# todo: Subscribe / Unsubscribe button
# todo: API Request

# ! Scraping ====================
# * Needs Better Selenium Implementation
# * Solve The Different Sources Problem
# * Always Check for Time
# * Bypass CDN
# * Split based on the dot to give more importance for bigger texts
# * better logging for time tag
# todo: Pop-up ads

# ! ModelAnalsis.py =============
# todo: Parameters Tuning

# ! Additional Tasks ============
# * Logging system 
# todo: parallel execution
# todo: Explaining Basic Concepts

# ! Testing =====================
# * Testing System to check for accuracy
# * False Positives and different projections to be saved
# * More Tests
# * CI implementation
# todo: plots

# ! =============================


# Load Web Driver
def get_driver():
    chrome_options = uc.ChromeOptions()
    # chrome_options.add_argument("--headless=new")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.page_load_strategy = 'eager' 
    driver = uc.Chrome(options=chrome_options) 
    return driver


# Check for recent news
def is_recent(date,threshold):
    current_date = datetime.now()
    day_limit = current_date - timedelta(days=threshold + 1)
    post_date = dateparser.parse(date)
    return post_date >= day_limit

# Retrieve news from each post and feed it to The Great Filter
def get_news_from_post(index, Source, driver, hist_index):

    # Go To Posts Page
    query = Source["post"] + (f" {Source["click"]}" if Source["click"] != "<self>" else "")
    driver.execute_script("window.history.pushState({}, '', document.URL);")
    driver.execute_script(f"document.querySelectorAll('{ query }')[{ index }].click();")
    time.sleep(WAITING_TIME)
    html = driver.page_source

    # The Great Filter in action    
    pure_news = filter_html(html)

    # Save Found News to a file
    name = Source["source"] + " Post " + str(hist_index)
    with open(f"./ExtractedNews/{ name }.txt", "w") as f:
        f.write(driver.current_url + "\n" + "\n".join(pure_news))

    # Close Tab if new one is created, go back if none is created
    tabs = driver.window_handles
    if (len(tabs) > 1):
        driver.switch_to.window(tabs[-1]) 
        driver.close()
        driver.switch_to.window(tabs[0])
    else :
        driver.back()
        driver.refresh()
        time.sleep(WAITING_TIME)

    return pure_news

def get_available_posts(html, Source, driver, history):
    # Process HTML content to find and extract new posts within time threshold while avoiding duplicates
    soup = BeautifulSoup(html, "html.parser")
    posts = soup.select(Source["post"])

    # Finding recent posts
    post_gathered = []
    for i, post in enumerate(posts):

        # Check if the post is already in history
        comparing_length = math.floor(len(post.get_text(separator=" ").strip()) * IS_SIMILAR)
        if any(post.get_text(separator=" ").strip()[:comparing_length] in history_log for history_log in history):
            continue
        
        # Check if the post contains the expected time tag and if it's recent
        if (post.select_one(Source["time"])):
            post_time = post.select_one(Source["time"])
            if (is_recent(post_time.get_text(separator=" ").strip(), THRESHOLD)):
                history.append(post.get_text(separator=" ").strip())
                print(str(len(history)) + " | " + post.get_text(separator=" ").strip())
                pure_news = get_news_from_post(i,Source, driver, len(history))
                post_gathered.append(pure_news)

        elif len(post_gathered) == 0 and i == len(posts) - 1: 
            message = f"\n ============= Error finding time in {Source["source"]} ============== \n {post.select_one(Source["time"])} \n {Source["time"]} \n ======================================\n"
            print(f"Post doesn't contain expected time : {message}")
            generate_logs(Source["url"], "Time Tag Not Found", post)
    
    return post_gathered


def process_source(Source):
    posts_gathered = []
    driver = get_driver()
    try : 
        history = []
        print("="*50)
        driver.get(Source["url"])

        # scroll and wait for posts to load
        for i in range(SCROLL):
            WebDriverWait(driver, WAITING_TIME*3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, Source["post"]))
            )
            time.sleep(WAITING_TIME)
            html = driver.page_source
            available_posts = get_available_posts(html, Source, driver, history)
            if len(available_posts) != 0:
                posts_gathered.extend(available_posts)
            
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
            
    except Exception as e:
        generate_logs(Source["url"], "Exception", e, traceback.format_exc())
    
    driver.quit()
    return posts_gathered


def publish(html):
    pass
    # api request

# Get Recent News
def main():

    # Load Sources from file
    with open("Sources.json") as f:
        Sources = json.loads(f.read())
    
    # Ahead Start
    Sources = Sources[2::6]


    # Iterate through the sources
    for Source in Sources:
        process_source(Source)

    # if __name__ == '__main__':
    # with futures.ProcessPoolExecutor() as executor:
    #     posts = list(executor.map(process_source, Sources))
    # for post_by_source in posts:
    #     print(post_by_source)
    #     print("="*50)
    # code_html = nexus(results)
    # publish(code_html)


main()