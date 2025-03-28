import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN

from main import fetch_text

from bs4 import BeautifulSoup


MIN_LIMIT = 32


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
        div_text = [t.get_text(separator="\n").strip() for t in div.find_all(text=True) if t.parent.name not in text_headers]
        text_list.extend(div_text)

    # Text Preprocessing
    filtered_text_list = [text for text in text_list if len(text) >= MIN_LIMIT and not np.any([(symbol in text) for symbol in forbidden_characters])]
    return list(set(filtered_text_list))


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
# main("https://www.aljazeera.com/news/2025/3/9/syrias-president-calls-for-peace-calm-amid-brutal-clashes", 1.2, 8, "euclidean")
