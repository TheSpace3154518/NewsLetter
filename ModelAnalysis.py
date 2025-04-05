from TheGreatFilter import extract_text, perform_dbscan
from constants import *
from sentence_transformers import SentenceTransformer

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt
import numpy as np





def plot_projection(global_projection, labels, texts, Title, axs):

    projection_clusters = [global_projection[labels == label] for label in np.unique(labels)]

    all_colors = ["black", "red","blue","green", "yellow", "pink", "purple", "gray", "brown", "magenta"]
    axs.set_title(Title)
    for index,cluster in enumerate(projection_clusters):
        if index == 0:
            axs.scatter(
                cluster[:, 0],
                cluster[:, 1], 
                s=10,
                color=all_colors[index],
                # marker="X"
            )
        else :
            axs.scatter(
                cluster[:, 0],
                cluster[:, 1], 
                s=10,
                color=all_colors[index],
            )

    min_coords = np.min(global_projection,axis=0)
    max_coords = np.max(global_projection,axis=0)

    # plot1.set_xlim(min_coords[0] - 1, max_coords[0] + 1)
    # plot1.set_ylim(min_coords[1] - 1, max_coords[1] + 1)

    axs.set_xlim(min_coords[0] - 1, max_coords[0] + 1)
    axs.set_ylim(min_coords[1] - 1, max_coords[1] + 1)



def Projection(html, axs):
    model = SentenceTransformer(model_name)
    texts = extract_text(html)
    if not texts:
        raise Exception("No text content extracted from the page.")

    # Compute embeddings for each text segment
    embeddings = np.array(model.encode(texts))
    labels = perform_dbscan(embeddings, texts,EPS,MIN_SAMPLES)


    pca = PCA(n_components=min(30,len(embeddings)))
    X_pca = pca.fit_transform(embeddings)
    tsne = TSNE(n_components=2, perplexity=min(30,len(embeddings) - 1), random_state=42)
    embeddings_final = tsne.fit_transform(X_pca)
    plot_projection(embeddings_final, labels,texts, "PCA + T-SNE", axs[0])

    tsne = TSNE(n_components=2, perplexity=min(30,len(embeddings) - 1), random_state=42)
    embeddings_tsne = tsne.fit_transform(embeddings)
    plot_projection(embeddings_tsne, labels,texts, "T-SNE", axs[1])

    plt.tight_layout()
    plt.show()

    
    print("Done")