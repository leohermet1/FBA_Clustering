import os
from natsort import os_sorted

import scipy.io as spio

import re

from sklearn.preprocessing import normalize
from sklearn.preprocessing import StandardScaler

import pandas as pd

from scipy.io import loadmat


import numpy as np

from scipy.io import savemat






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

# definition of the function that get the solution matrice of a patient from the path of a .mat file

def getSol(path):
    # load the matlab structure
    load = spio.loadmat(path)

    # get the structure array
    structure = load['sampleMetaOutC']

    # get solution space matrix
    points = structure['points'][0, 0]  # row = reactions, col = solutions
    return points



### Remove the reaction fluxes equal to zero at every solution points and for every patient ###


def ReactionEqualtozeroForDifferentPatients(paths, avg):
    # browse every paths gived in arguments
    index_rfz_allPatients = {}
    for x in range(len(paths)):
        #every 3 file
        if x % 3 == 0:
            #get the ID
            pID = re.search(r'\d+', paths[x]).group()
            p1 = getSol(paths[x])
            p2 = getSol(paths[x+1])
            p3 = getSol(paths[x+2])
            #get the full matrix of the patient
            if avg == True:
                p = p2
            else:
                p = np.concatenate((p1,p2,p3),axis=1)
            print(pID,p.shape)
            index_rfz = []
            # for each rows (reaction fluxes)
            for r in range(p.shape[0]):
                # check if every value of the row is equal to zeros
                if len(np.where(p[r] == 0)[0]) == (p.shape[1]):
                    # append the index of the reaction fluxes with all values equal to zeros
                    index_rfz.append(r)
            # get the reaction fluxes that are equal to zero for each patients
            index_rfz_allPatients["p{0}".format(pID)] = index_rfz

    return index_rfz_allPatients


# function that get the index of the reaction fluxes that equal to 0 in every patients
def getReactionEqualtozeroforEveryPatients(index_rfz_allPatients):
    # Flag to check if all elements are same
    res = True

    # extracting value to compare
    pat1 = list(index_rfz_allPatients.values())[0]

    # check if all reactions in each patients are the same
    for pat in index_rfz_allPatients:
        if index_rfz_allPatients[pat] != pat1:
            res = False
            break

    # if every reactions are the same
    if res:
        # get the list of reactions of the first patient
        reactionFluxesZ = pat1
        print('Every patients have the same list of reaction fluxes equal to 0 for every solution points')
        print('This list is composed of', len(reactionFluxesZ), 'reaction fluxes')

    else:
        reactionFluxesZ = None
        print('The reactions equal to 0 for every solution points are not the same for every patients')
    return reactionFluxesZ


# definition of the function that normalize a matrix using StandardScaler
def norm(matrix):
    # normalize
    matrixT = matrix.transpose()
    zscore = StandardScaler().fit(matrixT)
    X_zT = zscore.transform(matrixT)
    X_z = X_zT.transpose()

    return X_z



### Correlation analysis ###


# Definition of the function that compute the correlation analysis (between rf) on normalized and reduced(rfz) matrices
# and return the reaction fluxes that can be removed in every single patients (threshold = 0.999)
def correlationAnalysis(paths, rfzeros_to_remove, avg):
    reactions_to_remove_comparison = []
    thresh = 0.999
    # browse every paths gived in arguments
    for x in range(len(paths)):
        # every 3 file
        if x % 3 == 0:
            # get the ID
            pID = re.search(r'\d+', paths[x]).group()
            p1 = getSol(paths[x])
            p2 = getSol(paths[x + 1])
            p3 = getSol(paths[x + 2])
            if avg == True:
                p = p2
            else:
                p = np.concatenate((p1, p2, p3), axis=1)

            # get the boolean list where true values corresponds to the index of the rf to remove
            tot_rf = int(p.shape[0])
            mask = np.zeros(tot_rf, dtype='bool')
            mask[rfzeros_to_remove] = True
            # get the reduced matrix (without reaction fluxes equal to zero) of the patient
            df = pd.DataFrame(p)
            p_reduced_rfzeros = np.array(df[~mask])
            # normalize the matrix
            pNorm_reduced_RFzeros = norm(p_reduced_rfzeros)
            print('\nPatient', pID, ':')
            print('Reaction fluxes equal to zero removed ---', pNorm_reduced_RFzeros.shape)

            ## Correlation analysis
            # get the solution matrice of the patient
            m = pNorm_reduced_RFzeros
            # transpose the matrix in order to do the correlation analysis on reaction fluxes
            # (correlation matrix computed on rows by default)
            mt = m.transpose()
            dft = pd.DataFrame(mt)
            # correlation analysis
            corrMatrix = dft.corr()
            dft.fillna(1)
            # boolean list on which reaction will be removed
            msk = np.tril(corrMatrix > thresh, k=-1).any(axis=1)
            # add the index of the reactions fluxes that are removed for each patient to a list
            reactions_to_remove_comparison.append(np.where(msk)[0].tolist())
            print('Correlation analysis ---', len(np.where(msk)[0].tolist()), 'reaction fluxes to remove')

    # get the reaction fluxes that can be removed in every single patients
    rf_to_remove_Corr = list(set.intersection(*map(set, reactions_to_remove_comparison)))

    return rf_to_remove_Corr, reactions_to_remove_comparison


# definition of the function that remove the reaction fluxes that have a correlation threshold > 0,999 (computed with the correlationAnalysis function)
# from the normalized and reduced (rfz) patient matrices
def removeReactionFluxesCorr(paths, rfzeros_to_remove, rf_to_remove_Corr, avg, dir):
    # browse every paths gived in arguments
    for x in range(len(paths)):
        # every 3 file
        if x % 3 == 0:
            # get the ID
            pID = re.search(r'\d+', paths[x]).group()
            p1 = getSol(paths[x])
            p2 = getSol(paths[x + 1])
            p3 = getSol(paths[x + 2])
            if avg == True:
                p = p2
            else:
                p = np.concatenate((p1, p2, p3), axis=1)

            ## Remove reaction fluxes that are equal to zero in every solution points
            # get the boolean list where true values corresponds to the index of the rf to remove 
            tot_rf = int(p.shape[0])
            mask = np.zeros(tot_rf, dtype='bool')
            mask[rfzeros_to_remove] = True
            # get the reduced matrix (without reaction fluxes equal to zero) of the patient
            df = pd.DataFrame(p)
            p_reduced_rfzeros = np.array(df[~mask])
            # normalize the matrix
            pNorm_reduced_RFzeros = norm(p_reduced_rfzeros)
            print('\nPatient', pID, ':')
            print('Reaction fluxes equal to zero removed ---', pNorm_reduced_RFzeros.shape)

            ## Remove reaction fluxes that are correlated
            # get the total number of reaction fluxes in m
            tot_rf = int(pNorm_reduced_RFzeros.shape[0])
            # get the boolean list where true values corresponds to the index of the rf to remove
            mask = np.zeros(tot_rf, dtype='bool')
            mask[rf_to_remove_Corr] = True
            df = pd.DataFrame(pNorm_reduced_RFzeros)
            print('Reaction fluxes correlated removed ---', df[~mask].shape)
            # get the full reduced matrix (without reaction fluxes equal to zero and the ones that are correlated) 
            # of the patient
            savemat(dir+'/p{0}_reduced_RF_ZeroAndCorr.mat'.format(pID),
                    {'mydata': df[~mask].to_numpy()})





