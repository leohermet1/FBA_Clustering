import argparse
import preprocessing1_functions as pp
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('path', help= 'Path of directory with .mat files')
parser.add_argument('-avg', help= 'Compute the preprocessing only on the mean .mat files')
parser.add_argument('-svd', type=int, help= 'Input(int): Number of component for the SVD')
parser.add_argument('-td', type=int, help= 'Input(int): Number of component for the tensor decomposition')
parser.add_argument('-npy', type=str, help= 'Input(str): Directory of the output of the tensor decomposition')
args = parser.parse_args()


# get the paths of all the .mat files
matDir = args.path
paths = pp.getPaths(matDir)

# Compute normalization and SVD for each patient
if args.svd:
    nb_components = args.svd
else:
    nb_components = 100
tensor = pp.getNormSVD(paths, nb_components)

# Compute tensor decomposition on the 3-way tensor
if args.td:
    rank = args.td
else:
    rank = 10
est_A_normalised, est_B_normalised, est_C_normalised = pp.tensorDecomposition(tensor, rank)

# Save pre-processed data as numpy file in the current directory
if args.npy:
    dir = args.npy
    np.save(dir+'/patientsMatrix.npy', est_A_normalised)
    np.save(dir+'/reactionFluxesMatrix.npy', est_B_normalised)
    np.save(dir+'/solutionPointsMatrix.npy', est_C_normalised)
else:
    np.save('patientsMatrix.npy', est_A_normalised)
    np.save('reactionFluxesMatrix.npy', est_B_normalised)
    np.save('solutionPointsMatrix.npy', est_C_normalised)



    

    

