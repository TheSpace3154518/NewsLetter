import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN

from WebWithinReach import fetch_text

from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5",
}
MIN_LIMIT = 20

# * JavaScript Rendering
# todo: Handle The Pictures issue
# todo: exploratory data analysis
# todo: More Tests

def extract_text(html):

    soup = BeautifulSoup(html, "html.parser")
    # Remove script and style elements
    for element in soup(["script", "style"]):
        element.decompose()

    # Get text
    text_headers = ["p", "h1", "h2", "h3", "h4", "h5", "h6","span"]
    tags = soup.find_all(text_headers)
    text_list = [text.get_text().strip() for text in tags if text.get_text().strip() and len(text.get_text()) >= 25]
    for img in soup.find_all("img"):
        alt_text = img.get("alt", "nothing")
        text_list.append("Picture describing " + alt_text)
    # print("\n".join(text_list))
    return list(set(text_list))


def compute_embeddings(texts, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts)
    return embeddings


def perform_dbscan(embeddings, texts, eps=0.5, min_samples=2, metric="euclidean"):
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric=metric).fit(embeddings)
    labels = clustering.labels_

    # Filter out noise (-1 label)
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


def main(url, eps=0.5, min_samples=2, metric="euclidiean"):
    html = fetch_text(url)
    texts = extract_text(html)
    if not texts:
        raise Exception("No text content extracted from the page.")

    # Compute embeddings for each text segment
    embeddings = compute_embeddings(texts)

    # Get Largest Cluster
    labels = perform_dbscan(embeddings, texts, eps, min_samples, metric)
    largest_cluster_texts = get_largest_cluster(texts,labels)
    # for i in largest_cluster_texts:
    #     print(i)
    #     t = input("Wait : ")
    return largest_cluster_texts


# main("https://x.com/OpenAI", 0.5, 2, "euclidean")
# main("https://www.aljazeera.com/news/2025/3/9/syrias-president-calls-for-peace-calm-amid-brutal-clashes", 0.5, 2, "euclidean")
