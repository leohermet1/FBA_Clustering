import argparse
import numpy as np
import visualization_functions as v


parser = argparse.ArgumentParser()
parser.add_argument('pathPatientsMatrix', help= 'Input(str): Path of the patients matrix (from the preprocessing run) as .npy file')
parser.add_argument('-sse', help= 'Compute SSE and Silhouette curves to chose the number of clusters for the patient matrix')
parser.add_argument('-metaboGrps', nargs="+", type=int, help= 'Input(list): Metabolic groups for each patients')
parser.add_argument('-cl', type=int, help= 'Input(int): Compute and visualize a number of clusters on the patient matrix')
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
    v.computeK(patientsMatrix, 10)

if args.cl:
    nb_clusters = args.cl
    clusters = getCl_K(patientsMatrix, nb_clusters)
    v.saveIMG(Xt, v1, v2, 'PCA of the patients with computed clusters', 'PCA_patients_cl.svg', clusters)

if args.metaboGrps:
    clusters = [patGrp - 1 for patGrp in args.metaboGrps]
    v.saveIMG(Xt, v1, v2, 'PCA of the patients with metabolo groups', 'PCA_patients_Mgrp.svg', clusters)



## Visualization of the reaction fluxes matrix ##

if args.pathRF:
    reactionFluxesMatrix = np.load(args.pathRF)
    Xt, v1, v2 = cl.PCA(reactionFluxesMatrix)
    cl.saveIMG(Xt, v1, v2, 'PCA of the reaction fluxes', 'PCA_RF.svg')



## Visualization of the solution points matrix ##

if args.pathSP:
    solutionPointsMatrix = np.load(args.pathSP)
    Xt, v1, v2 = cl.PCA(solutionPointsMatrix)
    cl.saveIMG(Xt, v1, v2, 'PCA of the solution points', 'PCA_SP.svg')