from sklearn.decomposition import PCA

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pandas as pd

import matplotlib.pyplot as plt

import numpy as np

from itertools import permutations



# function that compute the PCA and get the reactions that explain most of the variance
pca = PCA()

def PCA(matrix):
    # PCA
    Xt = pca.fit_transform(matrix)
    v1 = 'axis 1 = ' + str(round(pca.explained_variance_ratio_[0] * 100, 2)) + '%'
    v2 = 'axis 2 = ' + str(round(pca.explained_variance_ratio_[1] * 100, 2)) + '%'

    return Xt, v1, v2

def saveIMG(data, v1, v2, title, image_name, cl = False, clusters=None, cl_name=None):
    #visualization of the PCA
    fig, ax = plt.subplots()
    if cl:
        sc = ax.scatter(data[:, 0], data[:, 1], c=clusters)
        ax.legend(*sc.legend_elements(), title=cl_name)
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
    fig, ax = plt.subplots()
    plt.plot(range(2,kmax),sse,"o-")
    plt.ylabel("SSE")
    plt.xlabel('k')
    plt.title('SSE')
    fig.savefig('SSE_curve.svg', format='svg')
    #similarity within the cluster
    fig, ax = plt.subplots()
    plt.plot(range(2,kmax),silhouette,"o-")
    plt.ylabel("Silhouette")
    plt.xlabel('k')
    plt.title('Similarity within the cluster')
    fig.savefig('Silhouette_curve.svg', format='svg')


# definition of the function that compute the k-clusters of a matrix
def getCl_K(matrix, nb_clusters):
    # kmean clustering
    clusters = KMeans(nb_clusters).fit_predict(matrix)

    return clusters

### Comparison with the metabo groups ###

def getIdentityPerc(clusters, reel_cl):
    clustersNS = clusters.copy()
    # get the lists of clusters names and counts
    values, counts = np.unique(clustersNS, return_counts=True)
    cl = np.stack((values, counts))

    # get all the permutation of the clusters values
    lst = list(permutations(values))

    # get the percentage for
    best_perScl = 0
    for per in range(len(lst)):
        cl_s = cl[:, lst[per]]
        # order clusters
        c = 0
        for j in range(np.unique(reel_cl).shape[0]):
            for i in np.where(clustersNS == cl_s[0, j])[0]:
                clusters[i] = c
            c += 1

        # get position where cl are the same
        crc = np.column_stack((clusters, reel_cl))
        pTR = np.where(crc[:, 0] == crc[:, 1])[0]

        # get the percentage of same clusters
        perScl = round(pTR.shape[0] / len(clusters) * 100, 2)

        if perScl > best_perScl:
            best_perScl = perScl
            best_permutation = lst[per]
            best_clusters = clusters.copy()

    return best_perScl, best_permutation, best_clusters

def distClusters(best_clusters, reel_clusters):
    fig, ax = plt.subplots()
    plt.hist([best_clusters, reel_clusters], label=['Kmean clusters', 'Metabolic groups'])
    plt.xlabel('Clusters')
    plt.ylabel('Number of patients')
    plt.title('Distribution of the clusters')
    plt.legend()
    #save the plot as svg file
    fig.savefig('clusterDistribution.svg', format='svg')

def identicalClusters(best_clusters, reel_clusters):
    crc = np.column_stack((best_clusters, reel_clusters))
    pTR = np.where(crc[:, 0] == crc[:, 1])[0]
    print(round((pTR.shape[0] / len(best_clusters)) * 100, 2), '% of clusters are the same')
    print('\nPatients that are in the same cluster:', pTR)

    # plot patients with identicall clusters
    x = ['0', '1', '2', '3']
    y = [np.count_nonzero(crc[pTR][:, 0] == 0), np.count_nonzero(crc[pTR][:, 0] == 1),
         np.count_nonzero(crc[pTR][:, 0] == 2), np.count_nonzero(crc[pTR][:, 0] == 3)]
    fig, ax = plt.subplots()
    plt.bar(x, y)
    plt.xlabel('Clusters')
    plt.ylabel('Number of patients')
    plt.title('Patients with identicall clusters')
    # save the plot as svg file
    fig.savefig('identicalClusters.svg', format='svg')
