### imports ###

import os
from natsort import os_sorted

import scipy.io as spio

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from sklearn.preprocessing import StandardScaler

import re

import numpy as np



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
    paths = os_sorted(p)

    return paths



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



### Min, mean and max matrices as 3 distinct models ###


# definition of the function that normalize the matrices
def norm(matrix):
    # normalize
    matrixT = matrix.transpose()
    zscore = StandardScaler().fit(matrixT)
    X_zT = zscore.transform(matrixT)
    X_z = X_zT.transpose()

    return X_z


# function that compute the PCA and get the components (reaction fluxes) that explain most of the variance
pca = PCA()
def PCA_sol(matrix, pID, dir):
    # colormap of the classes
    clm = np.array(['red', 'green', 'blue'])
    mimema = np.repeat(clm, matrix.shape[0]/3)

    # PCA
    Xt = pca.fit_transform(matrix)
    v1 = 'axis 1 = ' + str(round(pca.explained_variance_ratio_[0] * 100, 2)) + '%'
    v2 = 'axis 2 = ' + str(round(pca.explained_variance_ratio_[1] * 100, 2)) + '%'

    # visualization of the PCA
    plt.scatter(Xt[:, 0], Xt[:, 1], c=mimema)
    plt.xlabel(v1, fontsize=10)
    plt.ylabel(v2, fontsize=10)
    pop_a = mpatches.Patch(color='red', label='Max')
    pop_b = mpatches.Patch(color='green', label='Mean')
    pop_c = mpatches.Patch(color='blue', label='Min')
    plt.legend(handles=[pop_a, pop_b, pop_c])
    plt.savefig(dir+"/Patient_Sampled_{0}_MaxMeanMin.svg".format(pID),
                format="svg")


# Definition of the function that normalize min, mean and max matrices from a given directory path
def norm3models(paths, dir):
    patientsM = {}
    nb_pat = round(int(len(paths)) / 3)
    print('\nVisualization of min, mean and max')
    print('-------------------------------------------------')

    for p in range(nb_pat):
        # get the position of the patient and his ID
        pos = p * 3
        pID = re.search(r'\d+', paths[pos]).group()

        # concatenate matrices Max, Mean and Min
        p1 = getSol(paths[pos])
        p2 = getSol(paths[pos + 1])
        p3 = getSol(paths[pos + 2])
        m = np.concatenate((p1, p2, p3), axis=1)
        mz = norm(m)

        # transpose the matrix to fit the pca on solution points (rows)
        mzT = mz.transpose()
        # visualization of the solution points on 2 components (PCA)
        PCA_sol(mzT, pID, dir)
        print('patient',pID,'done')