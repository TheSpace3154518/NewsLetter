import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN

import time

from bs4 import BeautifulSoup

from selenium import webdriver

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5",
}
MIN_LIMIT = 20

# * JavaScript Rendering
# todo: Handle The Pictures issue
# todo: exploratory data analysis
# todo: More Tests

def fetch_and_extract_text(url):

    # Fetch HTML Page
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options) 

    driver.get(url)
    time.sleep(10)
    html = driver.page_source
    driver.quit()



    soup = BeautifulSoup(html, "html.parser")
    # Remove script and style elements
    for element in soup(["script", "style"]):
        element.decompose()

    # Get text
    text_headers = ["p", "h1", "h2", "h3", "h4", "h5", "h6","span"]
    tags = soup.find_all(text_headers)
    text_list = [text.get_text().strip() for text in tags if text.get_text().strip() and len(text.get_text()) >= 25]
    # for img in soup.find_all("img"):
    #     alt_text = img.get("alt", "nothing")
    #     text_list.append("Picture describing " + alt_text)
    print("\n".join(text_list))
    return list(set(text_list))


def compute_embeddings(texts, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts)
    return embeddings


def perform_dbscan(embeddings, texts, eps, min_samples, metric):
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric=metric).fit(embeddings)
    labels = clustering.labels_

    # Filter out noise (-1 label)
    cluster_ids = [label for label in labels if label != -1]
    if not cluster_ids:
        # if no cluster is identified, return all texts
        return texts

    # Count occurrences of each cluster
    unique, counts = np.unique(cluster_ids, return_counts=True)
    largest_cluster = unique[np.argmax(counts)]
    selected_texts = [
        text for text, label in zip(texts, labels) if label == largest_cluster
    ]
    return selected_texts


def extract_main_news(url, eps, min_samples, metric):
    texts = fetch_and_extract_text(url)
    if not texts:
        raise Exception("No text content extracted from the page.")

    # Compute embeddings for each text segment
    embeddings = compute_embeddings(texts)

    # Get Largest Cluster
    largest_cluster_texts = perform_dbscan(embeddings, texts, eps, min_samples, metric)
    for i in largest_cluster_texts:
        print(i)
        t = input("Wait : ")
    return largest_cluster_texts


extract_main_news("https://x.com/OpenAI", 0.5, 2, "euclidean")
