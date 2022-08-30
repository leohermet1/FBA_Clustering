from sklearn.decomposition import PCA

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.cluster import Birch

from sklearn.cluster import SpectralClustering

import numpy as np



# function that compute the PCA and get the reactions that explain most of the variance
pca = PCA()

def PCA(matrix):
    # PCA
    Xt = pca.fit_transform(matrix)
    v1 = 'axis 1 = ' + str(round(pca.explained_variance_ratio_[0] * 100, 2)) + '%'
    v2 = 'axis 2 = ' + str(round(pca.explained_variance_ratio_[1] * 100, 2)) + '%'

    return Xt, v1, v2

def saveIMG(data, v1, v2, title, image_name, **clusters):
    #visualization of the PCA
    fig, ax = plt.subplots()
    if clusters:
        sc = ax.scatter(data[:, 0], data[:, 1], c=clusters, cmap='Wistia')
        ax.legend(*sc.legend_elements(), title='clusters')
    else:
        plt.scatter(data[:, 0], data[:, 1])
    plt.xlabel(v1, fontsize=10)
    plt.ylabel(v2, fontsize=10)
    plt.title(title)
    #save the plot as svg file
    fig.savefig(image_name, format='svg')

#definition of the function that shows the SSE and the similarity within the cluster for k = 2 : 10
def computeK(matrix,kmax):
    sse = {}
    silhouette = {}
    df = pd.DataFrame(matrix)
    for k in range(2,kmax):
        km = KMeans(k).fit(df)
        sse[k] = km.inertia_
        clusters =  km.predict(df)
        silhouette[k] = silhouette_score(df,clusters)
    sse = pd.Series(sse)
    silhouette = pd.Series(silhouette)
    #visualization SSE
    plt.plot(range(2,kmax),sse,"o-")
    plt.ylabel("SSE")
    plt.xlabel('k')
    plt.title('SSE')
    fig.savefig('SSE_curve', format='svg')
    #similarity within the cluster
    plt.plot(range(2,kmax),silhouette,"o-")
    plt.ylabel("Silhouette")
    plt.xlabel('k')
    plt.title('Similarity within the cluster')
    fig.savefig('Silhouette_curve', format='svg')


# definition of the function that compute the k-clusters of a matrix
def getCl_K(matrix, nb_clusters):
    # kmean clustering
    clusters = KMeans(nb_clusters).fit_predict(matrix)

    return clusters


# definition of the function that compute the clusters of a matrix using BIRCH Clustering
def getCl_BIRCH(matrix, nb_clusters):
    # define the model
    model = Birch(threshold=0.01, n_clusters=nb_clusters)
    # fit the model
    model.fit(matrix)
    # assign a cluster to each example
    clusters = model.predict(matrix)

    return clusters

def getCl_SC(matrix,nb_clusters):
    # train and predict
    clusters = SpectralClustering(n_clusters = nb_clusters, eigen_solver='arpack',
            affinity="nearest_neighbors").fit_predict(matrix)
    return clusters


