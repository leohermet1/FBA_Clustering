import os
from natsort import os_sorted

import scipy.io as spio

import re

from sklearn.preprocessing import normalize
from sklearn.preprocessing import StandardScaler

import pandas as pd

from scipy.io import loadmat


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


# definition of the function that get all the paths of the Mean.mat files
def getMeanP(paths):
    mP = []
    for p in paths:
        if p[-8:] == 'Mean.mat':
            mP.append(p)
    return mP



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


def ReactionEqualtozeroForDifferentPatients(paths):
    # browse every paths gived in arguments
    index_rfz_allPatients = {}
    for pm in paths:
        # get the ID
        pID = re.search(r'\d+', pm).group()
        # get the solution matrice of the patient
        p = getSol(pm)
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


#function that get the index of the reaction fluxes that equal to 0 in every patients
def getReactionEqualtozeroforEveryPatients(index_rfz_allPatients):
    l=[]
    #check if all reactions  in each patients are the same
    for i in index_rfz_allPatients.keys():
        for j in index_rfz_allPatients.keys():
            if index_rfz_allPatients[i] == index_rfz_allPatients[j]:
                l.append(j)
    reactionFluxesZ = None
    #check if we append every reactions 
    #which mean that every patients has the same reaction equal to zero
    if len(l)==len(index_rfz_allPatients.keys())**2:
        #get the list of reactions of a random patient since they are all the same
        reactionFluxesZ = index_rfz_allPatients[j]

    return reactionFluxesZ


# definition of the function that normalize a matrix using StandardScaler

def norm(matrix):
    # normalize
    matrixT = matrix.transpose()
    zscore = StandardScaler().fit(matrixT)
    X_zT = zscore.transform(matrixT)
    X_z = X_zT.transpose()

    return X_z


def removeReactionFluxesZ(paths, rf_to_remove):
    p_reducedR = {}
    for pm in paths:
        # get the ID
        pID = re.search(r'\d+', pm).group()
        # get the solution matrice of the patient
        p = getSol(pm)
        # normalize the matrix
        pz = norm(p)
        df = pd.DataFrame(pz)
        # get the boolean list where true values corresponds to the index of the rf to remove 
        tot_rf = int(pz.shape[0])
        mask = np.zeros(tot_rf, dtype='bool')
        mask[rf_to_remove] = True
        # get the reduced matrix (without reaction fluxes equal to zero) of the patient
        p_reducedR["p{0}".format(pID)] = np.array(df[~mask])

    return p_reducedR



### Correlation analysis ###


# Definition of the function that compute the correlation analysis (between rf) on normalized and reduced(rfz) matrices
# and return the reaction fluxes that are removed in every single patients (threshold = 0.999)
def correlationAnalysis(p_reduced_RFZ):
    reactions_to_remove_comparison = []
    thresh = 0.999
    #browse every paths gived in arguments
    for pID in p_reduced_RFZ.keys():
        #get the solution matrice of the patient
        m = p_reduced_RFZ[pID]
        #transpose the matrix in order to do the correlation analysis on reaction fluxes
        # (correlation matrix computed on rows by default)
        mt = m.transpose()
        dft = pd.DataFrame(mt)
        #correlation analysis
        corrMatrix = dft.corr()
        #boolean list on which reaction will be removed
        msk = np.tril(corrMatrix > thresh, k=-1).any(axis=1)
        #add the index of the reactions fluxes that are removed for each patient to a list
        reactions_to_remove_comparison.append(np.where(msk)[0].tolist())
        print('patient ',pID,' done ')
    # get the reaction fluxes that are removed in every single patients
    rf_to_remove = list(set.intersection(*map(set, reactions_to_remove_comparison))).sort()

    return rf_to_remove


# definition of the function that remove the reaction fluxes that have a correlation threshold > 0,999 (computed with the correlationAnalysis function)
# from the normalized and reduced (rfz) patient matrices
def removeReactionFluxesCorr(p_reduced_RFZ, rf_to_remove):
    p_reducedR = {}
    # browse every paths gived in arguments
    for pID in p_reduced_RFZ.keys():
        # get the solution matrice of the patient
        m = p_reduced_RFZ[pID]
        df = pd.DataFrame(m)
        # get the total number of reaction fluxes in m
        tot_rf = int(m.shape[0])
        # get the boolean list where true values corresponds to the index of the rf to remove
        mask = np.zeros(tot_rf, dtype='bool')
        mask[rf_to_remove] = True
        # get the reduced matrix (without reaction fluxes equal to zero) of the patient
        p_reducedR["{0}".format(pID)] = np.array(df[~mask])
        print(pID, ' done')

    return p_reducedR





