### imports ###

import os

import scipy.io as spio
from sklearn.preprocessing import StandardScaler

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
    return p

#definition of the function that get all the paths of the Mean.mat files
def getMeanP(paths):
    mP = []
    for p in paths:
        if p[-8:] == 'Mean.mat':
            mP.append(p)
    return mP



### Normalisation ###


# definition of the function that get the solution-reaciton matrices of a patient from the path of a .mat file
def getSol(path):
    # load the matlab structure
    load = spio.loadmat(path)

    # get the structure array
    structure = load['sampleMetaOutC']

    # get solution space matrix
    points = structure['points'][0, 0]  # row = reactions, col = solutions
    return points

# definition of the function that normalize the matrices and compute SVD with 1 component
def norm(matrix):
    # normalize
    matrixT = matrix.transpose()
    zscore = StandardScaler().fit(matrixT)
    X_zT = zscore.transform(matrixT)
    X_z = X_zT.transpose()

    return X_z

#definition of the function that compute the SVD with 1 component from multiple .mat files
def getNormM(paths):
    #create the dictionary for the svd matrices of each patients
    patients = {}
    #browse every paths gived in arguments
    for pm in paths:
        #get the solution matrice of the patient
        p = getSol(pm)
        #get the ID
        if pm[-11:-9].find('_') == 0:       #if there is a '_' in pm[-11:-9] so if the patient number <10
            pID = pm[-10:-9]
        #if pm[-11:-9].find('_') == -1
        else:
            pID = pm[-11:-9]
        print('Patient',pID)
        #get the normalized matrix
        pz = norm(p)
            #adding patient ID as key and svd as item for the dictionary
        patients["p{0}".format(pID)] = pz

    # create a list of all the patients id correctly sorted from p1 to p95
    nP = []
    for i in range(len(patients)):
        nP.append("p{0}".format(i + 1))

    # get all the normalized matrices in one using stack and a generator function
    norms = np.stack((patients[nP[i]] for i in range(len(patients))))
    
    #save the tensor as .npy file
    np.save('normMeanPats.npy', norms)

    return norms

