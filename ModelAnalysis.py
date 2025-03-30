from TheGreatFilter import extract_text, perform_dbscan
from main import fetch_text
from ModelTests import TestModel
from sentence_transformers import SentenceTransformer

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt
import numpy as np



# > ============ Constants ======================
EPS = 1.2
MIN_SAMPLES = 2
model_name="all-MiniLM-L6-v2"
url = "https://www.wired.com/"
model = SentenceTransformer(model_name)
# > =============================================


def plot_projection(global_projection, labels, texts, Title):

    projection_clusters = [global_projection[labels == label] for label in np.unique(labels)]
    text_clusters = [np.array(texts)[labels == label] for label in np.unique(labels)]

    all_colors = ["black", "red","blue","green", "yellow", "pink", "purple", "gray", "brown", "magenta"]
    fig3 = plt.figure()
    plot3 = fig3.add_subplot(111)
    plot3.set_title(Title)
    for index,cluster in enumerate(projection_clusters):
        print(f"----------------- {all_colors[index]} -------------------")
        for i in range(0,len(text_clusters[index])):
            print(str(i) + " | " + str(text_clusters[index][i].item()))
        print()
        if index == 0:
            plot3.scatter(
                cluster[:, 0],
                cluster[:, 1], 
                s=10,
                color=all_colors[index],
                # marker="X"
            )
        else :
            plot3.scatter(
                cluster[:, 0],
                cluster[:, 1], 
                s=10,
                color=all_colors[index],
            )

    min_coords = np.min(global_projection,axis=0)
    max_coords = np.max(global_projection,axis=0)

    # plot1.set_xlim(min_coords[0] - 1, max_coords[0] + 1)
    # plot1.set_ylim(min_coords[1] - 1, max_coords[1] + 1)

    plot3.set_xlim(min_coords[0] - 1, max_coords[0] + 1)
    plot3.set_ylim(min_coords[1] - 1, max_coords[1] + 1)




    


def Projection():
    html = fetch_text(url, 2)
    texts = extract_text(html)
    if not texts:
        raise Exception("No text content extracted from the page.")

    # Compute embeddings for each text segment
    print(f"\nThe Extracted text contains : {len(texts)}\n")
    embeddings = np.array(model.encode(texts))
    labels = perform_dbscan(embeddings, texts,EPS,MIN_SAMPLES)

    # umap_transform = umap.UMAP().fit(embeddings)
    # global_projection = umap_transform.transform(embeddings)
    # plot_projection(global_projection, labels,texts, "UMAP Projection")

    pca = PCA(n_components=min(30,len(embeddings)))
    X_pca = pca.fit_transform(embeddings)
    tsne = TSNE(n_components=2, perplexity=min(30,len(embeddings) - 1), random_state=42)
    embeddings_final = tsne.fit_transform(X_pca)
    plot_projection(embeddings_final, labels,texts, "PCA + T-SNE")

    tsne = TSNE(n_components=2, perplexity=min(30,len(embeddings) - 1), random_state=42)
    embeddings_tsne = tsne.fit_transform(embeddings)
    plot_projection(embeddings_tsne, labels,texts, "T-SNE")

    # Testing model wih chosen params
    # print("------------------ Results -----------------\n")
    # noise, missed, falses = TestModel("./Tests/Al-Jazeera.txt", EPS,MIN_SAMPLES,"euclidean")
    # print(f"Noise Included : {noise:.3f}")
    # print(f"Missed Data : {missed:.3f}")
    # print(f"Falsely Included : {"\n".join(falses)}")
    # print()
    # print("--------------------------------------------")


    plt.show()

    
    print("Done")


Projection()