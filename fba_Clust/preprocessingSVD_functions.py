### imports ###

import os
from natsort import os_sorted

import scipy.io as spio

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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
    print('\n')
    print(f'Normalization + SVD for {nb_components} components')
    print('-------------------------------------------------')
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
            varExp.append(var_explained)
            patients.append(p_svd)

    # get all the normalized and reduced matrices in one 3way tensor
    tensor = np.stack(patients, axis=0)
    #compute the mean of the explained variance for all the patients
    varExp_MEAN = np.sum(varExp, axis=0) / len(nP)
    print('\nThe average explained variance for SVD with', nb_components, 'components is:', round(varExp_MEAN * 100, 3),'%')
    
    return tensor


### tensor decomposition ###

def tensorDecomposition(tensor, rank):
    print('\n')
    print(f'Tensor decomposition for {rank} components')
    print('-------------------------------------------------')
    best_err = np.inf
    decomposition = None

    # Initialise and fit 5 models
    for run in range(5):
        print(f'Training model {run+1}...')
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
    print(f'\nBest model error: {best_err}')

    est_tensor = tl.parafac2_tensor.parafac2_to_tensor(decomposition)
    est_weights, (est_A, est_B, est_C) = tl.parafac2_tensor.apply_parafac2_projections(decomposition)

    #compute the reconstruction error
    reconstruction_error = la.norm(est_tensor - tensor)
    recovery_rate = 1 - reconstruction_error / la.norm(tensor)

    print(f'{recovery_rate:2.0%} of the data is explained by the model\n')

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