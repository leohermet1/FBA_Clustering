import argparse
import numpy as np
import visualization_functions as v


parser = argparse.ArgumentParser()
parser.add_argument('pathPatientsMatrix', help= 'Input(str): Path of the patients matrix (from the preprocessing run) as .npy file')
parser.add_argument('-sse', action='store_true', help= 'Compute SSE and Silhouette curves to chose the number of clusters for the patient matrix')
parser.add_argument('-cl', type=int, help= 'Input(int): Compute and visualize a number of clusters on the patient matrix')
parser.add_argument('-Mgrp', action='store_true', help= 'Add the metabolic groups to the distribution of the patients and compare them to the computed clusters')
parser.add_argument('-pathRF', help= 'Input(str): Path of the reaction fluxes matrix (from the preprocessing run) as .npy file')
parser.add_argument('-pathSP', help= 'Input(str): Path of the solution points matrix (from the preprocessing run) as .npy file')
args = parser.parse_args()


    
## Visualization and Clustering  of the patients matrix ##

# Load the patient matrix (output of the tensor decomposition)
patientsMatrix = np.load(args.pathPatientsMatrix)

# Compute the PCA of the patient matrix
Xt, v1, v2 = v.PCA(patientsMatrix)

# Save the plot distribution of the patients on 2 PCA component
v.saveIMG(Xt, v1, v2, 'PCA of the patients', 'PCA_patients.svg')

if args.sse:
    # Save the SSE and Silouhette curve to get the optimal number of clusters
    v.computeK(patientsMatrix, 10)

if args.cl:
    # Compute Kmean n clusters
    nb_clusters = args.cl
    clusters = v.getCl_K(patientsMatrix, nb_clusters)

    # Save the distribution with the computed clusters
    v.saveIMG(Xt, v1, v2, 'PCA of the patients with computed clusters', 'PCA_patients_Kcl.svg', cl =True, clusters=clusters, cl_name='clusters')

if args.Mgrp:
    # Initiate the metabolic groups of each patients
    metaboGrps = np.array([2, 0, 2, 3, 3, 3, 0, 0, 1, 3, 2, 3, 3, 2, 3, 2, 3, 2, 2, 1, 1, 3,
                   0, 3, 3, 3, 3, 3, 1, 2, 2, 3, 3, 2, 3, 1, 1, 2, 2, 2, 2, 2, 1, 3,
                   2, 3, 3, 1, 2, 3, 1, 0, 0, 3, 3, 1, 3, 0, 2, 3, 2, 2, 2, 2, 3, 3,
                   3, 3, 3, 0, 1, 3, 0, 3, 3, 0, 2, 3, 2, 2, 3, 2, 3, 3, 1, 2, 3, 3,
                   3, 0, 3, 3, 2, 0, 2])
    # Save the distribution with the metabolic groups
    v.saveIMG(Xt, v1, v2, 'PCA of the patients with metabolo groups', 'PCA_patients_Mgrp.svg', cl =True, clusters=metaboGrps, cl_name='metabo grps')

    # Compute Kmean with 4 clusters to be able to compare with the metabo groups
    clusters = v.getCl_K(patientsMatrix, 4)

    # Get the best permutation of the 4 computed clusters
    best_perScl, best_permutation, best_clusters = v.getIdentityPerc(clusters, metaboGrps)
    print('Higher percentage of identity: ', best_perScl)
    print('Corresponding permutation: ', best_permutation)

    # Save the distribution of the best permutation of the 4 computed clusters
    v.saveIMG(Xt, v1, v2, f'PCA with 4 computed clusters \n(optimal permutation with {best_perScl} % of identity)',
              'PCA_patients_optimal4cl.svg', cl =True, clusters=best_clusters, cl_name='clusters' )

    # Comparison of the distribution between the best permutation of the computed clusters against the metabolic groups
    v.distClusters(best_clusters, metaboGrps)

    # Distribution of the patients with identicall clusters between the best permutation of the computed ones and the metabolic groups
    v.identicalClusters(best_clusters, metaboGrps)



## Visualization of the reaction fluxes matrix ##

if args.pathRF:
    reactionFluxesMatrix = np.load(args.pathRF)
    Xt, v1, v2 = v.PCA(reactionFluxesMatrix)
    v.saveIMG(Xt, v1, v2, 'PCA of the reaction fluxes', 'PCA_RF.svg')



## Visualization of the solution points matrix ##

if args.pathSP:
    solutionPointsMatrix = np.load(args.pathSP)
    Xt, v1, v2 = v.PCA(solutionPointsMatrix)
    v.saveIMG(Xt, v1, v2, 'PCA of the solution points', 'PCA_SP.svg')