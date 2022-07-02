from sklearn.decomposition import PCA

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.cluster import Birch

from sklearn.cluster import SpectralClustering

import numpy as np

# function that compute the PCA and get the reactions that explain most of the variance

def PCA_sol(matrix):
    # PCA
    pca = PCA()
    Xt = pca.fit_transform(matrix)
    # visualization of the PCA
    fig, ax = plt.subplots()
    plot = plt.scatter(Xt[:, 0], Xt[:, 1])
    plt.show()

    # desciption of each axes
    for i in range(3):
        print('\nThe axe', i + 1, 'explain', round(pca.explained_variance_ratio_[i] * 100, 2), '% of the variance\n')

    return Xt

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
    plt.show()
    #similarity within the cluster
    plt.plot(range(2,kmax),silhouette,"o-")
    plt.ylabel("Silhouette")
    plt.xlabel('k')
    plt.title('Similarity within the cluster')
    plt.show()


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

def visClMeths(Xt,clList,matrix):
    # PCA to visualize the matrix
    #Xt = pca.fit_transform(matrix)

    for c in clList:
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20,5))
        clusters = getCl_K(matrix,c)
        scatter = ax1.scatter(Xt[:,0], Xt[:,1], c=clusters, label=np.unique(clusters))
        legend1 = ax1.legend(*scatter.legend_elements(), loc="upper right", title="Clusters")
        ax1.add_artist(legend1)
        ax1.set_title('Kmean clustering')
        clusters = getCl_SC(matrix,c)
        scatter = ax2.scatter(Xt[:,0], Xt[:,1], c=clusters)
        legend2 = ax2.legend(*scatter.legend_elements(), loc="upper right", title="Clusters")
        ax2.add_artist(legend2)
        ax2.set_title('Spectral clustering')
        clusters = getCl_BIRCH(matrix,c)
        scatter = ax3.scatter(Xt[:,0], Xt[:,1], c=clusters)
        legend2 = ax3.legend(*scatter.legend_elements(), loc="upper right", title="Clusters")
        ax3.add_artist(legend2)
        ax3.set_title('BIRCH clustering')
        plt.show()

