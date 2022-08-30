import os
from natsort import os_sorted

import scipy.io as spio

import re

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


# definition of the function that compute the SVD with 1 component from multiple .mat files
def getEucD(paths):
    # browse every paths gived in arguments
    patternID = []
    sorted_indexes = {}
    for pm in paths:
        # get the ID
        if re.search('Euc', pm) and re.search(r'\d+', pm):
            pID = re.search(r'\d+', pm).group()
            patternID.append('p' + pID + '_')
            load = spio.loadmat(pm)
            NED = load['NormalizedEuclideanDistance']
            sorted_indexes["p{0}".format(pID)] = np.argsort(NED.flatten())

    return (sorted_indexes, patternID)

#definition of the function that compute the SVD with 1 component from multiple .mat files
def getSortedArrOfSol(paths, sorted_indexes, patternID):
    #browse every paths gived in arguments
    AOS_sorted = {}
    for pm in paths:
        for pat in patternID:
            if re.search('reduced_', pm) and re.search(pat, pm):
                pID = 'p'+re.search(r'\d+', pm).group()
                load = spio.loadmat(pm)
                AOS = load['ArrayOfSolutions']
                AOS_sorted["{0}".format(pID)] = AOS[:,sorted_indexes[pID]]
                print(pID,'done')

    return AOS_sorted


def saveTensor(AOS_sorted, dir):
    sol_dim = []
    for p in AOS_sorted.keys():
        sol_dim.append(AOS_sorted[p].shape[1])
    nb_max_solP = min(sol_dim)

    tensor_list = []
    for p in AOS_sorted.keys():
        tensor_list.append(AOS_sorted[p][:,0:nb_max_solP])
    tensor = np.array(tensor_list)

    return tensor