import requests
from bs4 import BeautifulSoup
import re
import numpy as np
from sklearn.cluster import DBSCAN
from sentence_transformers import SentenceTransformer


def fetch_and_extract_text(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page, status code {response.status_code}")


    soup = BeautifulSoup(response.text, "html.parser")

    # Remove script and style elements
    for element in soup(["script", "style"]):
        element.extract()

    # First, try to extract text from <p> tags (usually main content)
    #todo: add h1,h2,div,header, pic's alts...
    paragraphs = soup.find_all("p")
    text_list = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]


    # Fallback: if no paragraphs, use all visible text
    if not text_list:
        texts = soup.find_all(text=True)
        
        def is_visible(text):
            if text.parent.name in [
                "style",
                "script", 
                "head", 
                "title", 
                "meta", 
                "[document]"
            ]:
                return False
            if re.match("<!--.*-->", str(text)):
                return False
            return True
        
        visible_texts = filter(is_visible, texts)
        text_list = [text.strip() for text in visible_texts if text.strip()]

    return text_list


def compute_embeddings(texts, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts)
    return embeddings


def perform_dbscan(embeddings, eps=0.5, min_samples=2):
    # DBSCAN with cosine metric (note: sklearn’s DBSCAN expects a distance, so cosine similarity is transformed)
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric="cosine").fit(embeddings)
    return clustering.labels_


def get_largest_cluster_texts(texts, labels):
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


def extract_main_news_content(url):
    texts = fetch_and_extract_text(url)
    if not texts:
        raise Exception("No text content extracted from the page.")

    # Compute embeddings for each text segment
    embeddings = compute_embeddings(texts)

    # Adjust DBSCAN parameters as needed (eps and min_samples) depending on content
    labels = perform_dbscan(embeddings, eps=0.5, min_samples=2)

    # Get the texts in the largest cluster
    largest_cluster_texts = get_largest_cluster_texts(texts, labels)
    return largest_cluster_texts


if __name__ == "__main__":
    url = "https://www.aljazeera.com/news/2025/3/9/syrias-president-calls-for-peace-calm-amid-brutal-clashes"
    try:
        main_content = extract_main_news_content(url)
        print("Extracted Main News Content:\n")
        for i in main_content:
            print(i)
            test = input("Wait : ")
    except Exception as e:
        print("Error:", e)
