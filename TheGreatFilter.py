import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN

import re

from constants import *

from bs4 import BeautifulSoup

# ? =========== Scraping Principles =============
# ?     - targeted Tags : p, h1, h2 ,h3 ,h4 ,h5, h6, span, div (special treatment)
# ?     - Text Must be >= 32, the longer the richer with info
# ?     - Pictures are included as " Picture describing " + alt(Picture)  
# ?     - Trademarks are eliminated
# ? =============================================


def extract_text(html):

    soup = BeautifulSoup(html, "html.parser")
    # Remove script and style elements
    for element in soup(["script", "style"]):
        element.decompose()

    # Get text
    text_headers = ["p", "h1", "h2", "h3", "h4", "h5", "h6", "span", "a"]
    forbidden_characters = ["™", "℠", "®", "©"]
    tags = soup.find_all(text_headers)
    text_list = [text.get_text().strip() for text in tags if text.get_text().strip()]
    # Get Pictures
    for img in soup.find_all("img"):
        alt_text = img.get("alt", "nothing")
        text_list.append("Picture describing " + alt_text)
    
    # Get Div Text
    divs = soup.find_all(["div"])
    for div in divs:
        div_text = [t.get_text(separator="\n").strip() for t in div.find_all(string=True) if t.parent.name not in text_headers]
        text_list.extend(div_text)
    
    text_list = [re.sub(r"\.\ (?=[a-zA-Z0-9])", "\n", text.replace('\u00A0', ' ')) for text in text_list]

    # Remove empty strings and split by new lines
    split_text = []
    for text in text_list:
        if "\n" in text:
            split_text.extend(text.split("\n"))
        else:
            split_text.append(text)
    split_text = [text.strip() for text in split_text if text.strip()]
    
    # Text Preprocessing
    filtered_text_list = [text for text in split_text if len(text) >= MIN_LIMIT and not np.any([(symbol in text) for symbol in forbidden_characters])]
    return list(set(filtered_text_list))

def perform_dbscan(embeddings, texts, eps=0.5, min_samples=2, metric="euclidean"):
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric=metric).fit(embeddings)
    labels = clustering.labels_
    return labels

def get_largest_cluster(texts, labels):
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


def filter_html(html, eps=EPS, min_samples=MIN_SAMPLES):
    model = SentenceTransformer(model_name)
    texts = extract_text(html)

    # Compute embeddings for each text segment
    embeddings = model.encode(texts)

    # Get Largest Cluster
    labels = perform_dbscan(embeddings, texts, eps, min_samples)
    largest_cluster_texts = get_largest_cluster(texts,labels)
    return largest_cluster_texts


# Testing
# import requests
# response = requests.get("https://www.aljazeera.com/news/2025/3/9/syrias-president-calls-for-peace-calm-amid-brutal-clashes") 
# html = response.text
# filter_html(html, 1.2, 8)
