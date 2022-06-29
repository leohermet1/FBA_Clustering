import scipy.io as spio

from sklearn.preprocessing import StandardScaler

from sklearn.decomposition import TruncatedSVD

import os 

import re

import numpy as np

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

from kneed import KneeLocator


# definition of the function that get the solution matrice of a patient from the path of a .mat file

def getSol(path):
    # load the matlab structure
    load = spio.loadmat(path)

    # get the structure array
    structure = load['sampleMetaOutC']

    # get solution space matrix
    points = structure['points'][0, 0]  # row = reactions, col = solutions
    return points


# definition of the function that normalize the matrices and compute SVD with 1 component

def normSVD(matrix, nb_components):
    # normalize
    matrixT = matrix.transpose()
    zscore = StandardScaler().fit(matrixT)
    X_zT = zscore.transform(matrixT)
    X_z = X_zT.transpose()
    # SVD 100 component
    svd = TruncatedSVD(n_components=nb_components)
    X_svd = svd.fit_transform(X_z)

    # show the variance explained
    var_explained = svd.explained_variance_ratio_.sum()
    perc_var_explained = round(var_explained * 100, 2)
    print(nb_components, 'components explain', perc_var_explained, "% of the variance")

    return X_svd, perc_var_explained


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

#get the paths of all the .mat files
paths = getPaths('/Users/lhermet/Downloads/Trauma_Patien-specific_EC-GEM/')

LOWcomps = [1, 2, 5, 10, 20, 30, 40, 50, 60, 80, 100, 150, 200, 300, 350, 400, 450, 500, 600, 700, 800]
# create the dictionary for the var explained of each comp of each patients
patientsVar = {}
nP = []
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
        varExp = []
        print('patient ', pID, ': ')
        for c in LOWcomps:
            # get the svd matrix
            p_svd, perc_var_explained = normSVD(m, c)
            varExp.append(perc_var_explained)
        # adding patient ID as key and svd as item for the dictionary
        patientsVar["p{0}".format(pID)] = varExp

# get all the variances in one matrix using stack and a generator function
AvarExpLOWcomps = np.stack([patientsVar[nP[i]] for i in range(len(patientsVar))])
AvarExpLOWcomps_SUM = np.sum(AvarExpLOWcomps, axis = 0)
AvarExpLOWcomps_MEAN = AvarExpLOWcomps_SUM/len(paths)

print((AvarExpLOWcomps_MEAN))