from TheGreatFilter import filter_html
import requests
import time
from logs_system import generate_logs
import undetected_chromedriver as uc
import os
from datetime import datetime
from constants import *


# Load Web Driver
def get_url(url, method=0):
    if method == 0:
        # Use the default method
        chrome_options = uc.ChromeOptions()
        # chrome_options.add_argument("--headless")  
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.page_load_strategy = 'eager' 
        driver = uc.Chrome(options=chrome_options) 
        driver.get(url)
        time.sleep(WAITING_TIME)
        page_source = driver.page_source
        driver.quit()
        return page_source
    elif method == 1:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            generate_logs(url, "Failed to fetch the page", response.text)
            raise Exception(f"Failed to fetch the page. Status code: {response.status_code}")    

def process_post(url):
    
    html = get_url(url, 0)
    
    if ("Verify you are human" in html):
        generate_logs(url, "Captcha detected", html)
        html = get_url(url, 1)
    # The Great Filter in action
    pure_news = filter_html(html)
    if not pure_news:
        generate_logs(url, "No text content extracted from the page", html)
        raise Exception("No text content extracted from the page.")

    return pure_news

# Test Model against a file
def TestModel(filePath):
    with open(filePath, "r") as file:
        newsLines = file.read().split("\n")
        predictedLines = process_post(newsLines[0])
        newsLines.pop(0)
        missingLines = newsLines
        correct = 0
        falsePositives = 0
        falseIncluded = []

        for i, line in enumerate(newsLines):
            newsLines[i] = line.strip()

        for i, line in enumerate(predictedLines):
            predictedLines[i] = line.strip()

        for line in predictedLines:
            if any(line in newsline for newsline in newsLines):
                if any(line in newsline for newsline in missingLines):
                    correct += 1
                    missingLines = [newsline for newsline in missingLines if line not in newsline]
            else:
                falsePositives += 1
                falseIncluded.append(line)

        newsAccuracy = (correct / len(newsLines)) * 100
        noiseAccuracy = (falsePositives / (correct + falsePositives)) * 100
        return noiseAccuracy, newsAccuracy, falseIncluded, missingLines


def test_accuracy():
    directory = "Tests"
    extension = ".txt" 

    files = ["Tests/" + f for f in os.listdir(directory) if f.endswith(extension)]

    name = f"./Unit Tests/test-{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.txt"
    for file in files:
        noise, included, falsePositives, missing = TestModel(file)
        with open(name, "a") as f:
            f.write(f"> File : {file}\n")
            f.write(f"Noise Accuracy : {noise:.3f}%, News Accuracy : {included:.3f}%, False Positives : {len(falsePositives)}, Missing : {len(missing)} \n")
            if (falsePositives):
                f.write("="*50)
                f.write(f"\nFalse Positives : \n{'\n'.join(falsePositives)}\n")
            if (missing):
                f.write("="*50)
                f.write(f"\nMissing Lines : \n{'\n'.join(missing)}\n")
            f.write("\n\n" + "----------------"*50 + "\n\n")
        assert noise <= NOISE_LIMIT, f"Noise Accuracy is too high: {noise}%, file: {file}"
        assert included >= INCLUDED_LIMIT, f"News Accuracy is too low: {included}%, file: {file}"
        print(f"{file} - Test Passed ")



if __name__ == "__main__":
    test_accuracy()