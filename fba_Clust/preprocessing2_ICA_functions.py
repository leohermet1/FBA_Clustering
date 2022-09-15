import os
from natsort import os_sorted

import scipy.io as spio

import re

import pandas as pd

from scipy.io import loadmat

import numpy as np

import warnings
from sklearn.decomposition import FastICA
from scipy.spatial import distance




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



### Sort the solution points of each patient ###

def getEucD(paths):
    # browse every paths gived in arguments
    sorted_indexes = {}
    for pm in paths:
        # get the ID
        if re.search('EucDistances', pm) and re.search(r'\d+', pm):
            pID = re.search(r'\d+', pm).group()
            load = spio.loadmat(pm)
            NED = load['NormalizedEuclideanDistance']
            sorted_indexes["p{0}".format(pID)] = np.argsort(NED.flatten()).argsort(kind="heapsort")

    return sorted_indexes


def getSortedArrOfSol(paths, sorted_indexes):
    AOS_sorted = {}
    sol_dim = []
    #browse every paths gived in arguments
    for pm in paths:
        if re.search('ReducedBySol', pm):
            pID = 'p'+re.search(r'\d+', pm).group()
            load = spio.loadmat(pm)
            AOS = load['ArrayOfSolutions']
            AOS_sorted["{0}".format(pID)] = AOS[:,sorted_indexes[pID]]
            sol_dim.append(AOS[:,sorted_indexes[pID]].shape[1])
            print(pID,'-',AOS[:,sorted_indexes[pID]].shape[1],'solution points')

    return AOS_sorted, sol_dim


def getMaxSol(AOS_sorted, sol_dim):
    nb_max_solP = min(sol_dim)
    print(nb_max_solP, 'solution points will be keep as maximum dimension for every patient')

    tensor_list = []
    for p in AOS_sorted.keys():
        tensor_list.append(AOS_sorted[p][:, 0:nb_max_solP])

    tensor = np.array(tensor_list)
    print('Size of the tensor :')
    print(tensor.shape)

    return tensor


### Reduce the solution points dimension with ICA ###

def getCentricSol(paths):
    # browse every paths gived in arguments
    centric_sol = {}
    for pm in paths:
        # get the ID
        if re.search('CentricSolution', pm) and re.search(r'\d+', pm):
            pID = re.search(r'\d+', pm).group()
            load = spio.loadmat(pm)
            centric_sol["{0}".format(pID)] = load['centricSolution']

    return centric_sol


def ICA(tensor,nb_comp,centric_sol,dir):
    i=1
    tensor_ICA = []
    for T in tensor:
        print('patient: ',i)
        # Compute ICA
        ica = FastICA(n_components=nb_comp, max_iter=1000).fit_transform(T)
        print(T.shape,' --- ',ica.shape)
        # get the euclidean distance from each components (feasible solution points)
        # to the centric solution point
        dst=[]
        for sol in ica.transpose():
            dst.append(distance.euclidean(centric_sol[str(i)].flatten(), sol))
        # get the indexes of the sorted distances
        sorted_indexes_comp = np.argsort(dst).argsort(kind="heapsort")
        # concatenate each patient's matrix to a tensor
        # with the components sorted by their distance to the centric solution point
        tensor_ICA.append(ica[:,sorted_indexes_comp])
        i+=1
    print('\nFinal tensor: ',np.array(tensor_ICA).shape)
    np.save(dir+f'/tensor_ICA_{nb_comp}.npy',np.array(tensor_ICA))


def multipleICA(tensor,componentList,centric_sol,dir):
    nb_warn = []
    for c in componentList:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            print('\nICA for',c,'components:')
            print('--------------------------------------------------')
            ICA(tensor,c,centric_sol,dir)
        nb_warn.append(len(w))
    print('\nList of components :',componentList)
    print('Number of patients with warning (for each ICA):', nb_warn)
