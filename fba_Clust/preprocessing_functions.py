### imports ###

import os
from natsort import os_sorted

import scipy.io as spio

from sklearn.preprocessing import normalize
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD

import re

import numpy as np

import tensorly as tl
from tensorly.decomposition import parafac2
import numpy.linalg as la



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

    return X_svd, var_explained

# definition of the function that normalize and compute the SVD for multiple .mat files

def getNormSVD(paths, nb_components):
    # create the dictionary for the var explained of each comp of each patients
    patients = []
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
            # get the svd matrix
            p_svd, var_explained = normSVD(m, nb_components)
            patients.append(p_svd)

    # get all the normalized and reduced matrices in one 3way tensor
    tensor = np.stack(patients, axis=0)
    #compute the mean of the explained variance for all the patients
    varExp_MEAN = np.sum(var_explained, axis=0) / len(nP)
    print('\nThe average explained variance for SVD with ', nb_components, 'is: ', round(varExp_MEAN, 3), '%')
    
    return tensor


### tensor decomposition ###

def tensorDecomposition(tensor, rank):
    print('---------------------------------------------------------------------------------------------')
    print(f'Number of components: {rank}')
    print('---------------------------------------------------------------------------------------------')
    print('\n')
    print('Normal dataset')
    print('--------------------------------------------------------------')
    best_err = np.inf
    decomposition = None

    # Initialise and fit 5 models
    for run in range(5):
        print(f'Training model {run}...')
        trial_decomposition, trial_errs = parafac2(tensor, rank, return_errors=True, tol=1e-8, n_iter_max=100,
                                                   random_state=run)
        print(f'Number of iterations: {len(trial_errs)}')
        print(f'Final error: {trial_errs[-1]}')
        #Chose the model with the lowest error in order to avoid local minima
        if best_err > trial_errs[-1]:
            best_err = trial_errs[-1]
            err = trial_errs
            decomposition = trial_decomposition
        print('-------------------------------')
    print('\n')
    print(f'Best model error: {best_err}')

    est_tensor = tl.parafac2_tensor.parafac2_to_tensor(decomposition)
    est_weights, (est_A, est_B, est_C) = tl.parafac2_tensor.apply_parafac2_projections(decomposition)

    #compute the reconstruction error
    reconstruction_error = la.norm(est_tensor - tensor)
    recovery_rate = 1 - reconstruction_error / la.norm(tensor)

    print(f'{recovery_rate:2.0%} of the data is explained by the model')
    print('\n')

    #get the matrices that represent each dimensions
    est_A, est_projected_Bs, est_C = tl.parafac2_tensor.apply_parafac2_projections(decomposition)[1]

    sign = np.sign(est_A)
    est_A = np.abs(est_A)
    est_projected_B = sign[:, np.newaxis] * est_projected_Bs

    est_A_normalised = est_A / la.norm(est_A, axis=0)
    est_Bs_normalised = [est_B / la.norm(est_B, axis=0) for est_B in est_projected_Bs]
    est_B_normalised = est_Bs_normalised[0]
    est_C_normalised = est_C / la.norm(est_C, axis=0)

    return (est_A_normalised, est_B_normalised, est_C_normalised)