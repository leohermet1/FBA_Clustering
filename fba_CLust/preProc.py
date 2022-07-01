### imports ###

import scipy.io as spio

from sklearn.preprocessing import StandardScaler

from sklearn.decomposition import TruncatedSVD

import os

import re

import numpy as np

from tensorly.decomposition import parafac2
import tensorly as tl

import time

import matplotlib.pyplot as plt




### Get the paths ###

#definition of the function that get all the paths of the .mat files
def getPaths(directory):
    p = []
    #browse every files in the directory
    for filename in os.listdir(directory):
        #only get the files that ends by '.mat'
        if filename.endswith(".mat") :
            p.append(os.path.join(directory, filename))
            continue
        else:
            continue
    return p



### Get the solutions matrices ###

# definition of the function that get the solution-reaciton matrices of a patient from the path of a .mat file
def getSol(path):
    # load the matlab structure
    load = spio.loadmat(path)

    # get the structure array
    structure = load['sampleMetaOutC']

    # get solution space matrix
    points = structure['points'][0, 0]  # row = reactions, col = solutions
    return points



### Normalisation and SVD ###

# definition of the function that normalize a matrix and compute SVD with nb_components

def normSVD(matrix, nb_components):
    # normalize
    matrixT = matrix.transpose()
    zscore = StandardScaler().fit(matrixT)
    X_zT = zscore.transform(matrixT)
    X_z = X_zT.transpose()
    # SVD n component
    svd = TruncatedSVD(n_components=nb_components)
    X_svd = svd.fit_transform(X_z)

    # show the variance explained
    var_explained = svd.explained_variance_ratio_.sum()
    perc_var_explained = round(var_explained * 100, 2)
    print(nb_components, 'components explain', perc_var_explained, "% of the variance")

    return X_svd, perc_var_explained

# definition of the function that normalize and compute the SVD for multiple .mat files

def getNormSVD(paths, nb_components):
    # sort the paths in order to have the Max, Mean and Min of each patients next to each others
    paths.sort()
    # create the dictionary for the var explained of each comp of each patients
    patients = {}
    nP = []
    varExp = []
    for x in range(len(paths)):
        # every 3 file
        if x % 3 == 0:
            # get the ID
            pID = re.search(r'\d+', paths[x]).group()
            nP.append("p{0}".format(pID))
            p1 = getSol(paths[x])
            p2 = getSol(paths[x + 1])
            p3 = getSol(paths[x + 2])
            m = np.concatenate((p1, p2, p3), axis=1)
            print('patient ', pID, ': ')
            # get the svd matrix and the percentage of variance explained
            p_svd, perc_var_explained = normSVD(m, nb_components)
            varExp.append(perc_var_explained)
            # adding patient ID as key and svd as item for the dictionary
            patients["p{0}".format(pID)] = p_svd

    # get all the normalized matrices in one using stack and a generator function
    norms = np.stack([patients[nP[i]] for i in range(len(patients))])
    #compute the mean of the explained variance for all the patients
    varExp_MEAN = np.sum(varExp, axis=0) / len(nP)

    return norms, varExp_MEAN


### tensor decomposition ###

def compute_reconstruction_err(tensor, reconstruction):
    rec_error = tl.norm(tensor - reconstruction) / tl.norm(tensor)
    return rec_error


def rec_error_cpANDparafac2(tensor, lComp):
    # init list of reconstruction error for each component
    rec_error_par2 = []
    par2_time = []

    for c in lComp:

        # parafac2 decomposition
        start = time.time()

        par = parafac2(tensor, c)
        par2_reconstruction = par.to_tensor()
        rec_error_par2.append(compute_reconstruction_err(tensor, par2_reconstruction))

        end = time.time()
        par2_time.append(round(end - start, 2))

        print('decomposition for', c, 'components done.')

    perc = 100
    perc_rec_error_par2 = [x * perc for x in rec_error_par2]

    # Plot another line on the same chart/graph
    plt.plot(lComp, perc_rec_error_par2, label="Parafac2 reconstruction error")

    plt.ylabel('% of reconstruction error')
    plt.xlabel('number of components')
    plt.title('Reconstruction error')
    plt.legend()
    plt.show()

    return rec_error_par2, par2_time