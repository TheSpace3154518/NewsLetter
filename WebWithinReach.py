from selenium import webdriver
import requests

import time


# todo : Needs Better Selenium Implementation
# todo : Solve The Different Sources Problem

def fetch_text(url, method=0):

    if (method == 0):
        response = requests.get(url)
        html = response.text
        return html
    elif (method == 1) :
        with open("SavedHTML.html", 'r') as f:
            html = f.read()
            return html
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.page_load_strategy = 'eager' 
    driver = webdriver.Chrome(options=chrome_options) 
    driver.get(url)
    time.sleep(60)
    html = driver.page_source
    with open("SavedHTML.html", "w") as f:
        f.write(html)
    driver.quit()
    return html