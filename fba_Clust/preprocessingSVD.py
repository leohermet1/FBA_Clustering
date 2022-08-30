import argparse
import preprocessingSVD_functions as pp
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('path', help= 'Path of directory with .mat files')
parser.add_argument('-mimema', type=str, help= 'Input(str): Name of the directory to save the .svg files'
                                     '\nVisualize the impact of the variance within the healthy patients'
                                     '\nThis option will save the distribution of the solution points for each patients as .svg files '
                                     '\n(search for 3 distinct groups represented by the min, mean and max matrices to see if we need all 3 models)')
parser.add_argument('-Avr', help= 'Compute the preprocessing only on the mean .mat files')
parser.add_argument('-svd', type=int, help= 'Input(int): Number of component for the SVD')
parser.add_argument('-td', type=int, help= 'Input(int): Number of component for the tensor decomposition')
parser.add_argument('-npy', type=str, help= 'Input(str): Directory of the output of the tensor decomposition')
args = parser.parse_args()


# get the paths of all the .mat files
matDir = args.path
paths = pp.getPaths(matDir)

# Visualize the impact of the variance within the healthy patients
# It will save the distribution of the solution points for each patients as .svg files
if args.mimema:
    dir = args.mimema
    pp.norm3models(paths, dir)

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
    rank = 15
est_A_normalised, est_B_normalised, est_C_normalised = pp.tensorDecomposition(tensor, rank)

# Save pre-processed data as numpy file in the current directory
if args.npy:
    dir = args.npy
    np.save(dir+'/est_A_normalised.npy', est_A_normalised)
    np.save(dir+'/est_B_normalised.npy', est_B_normalised)
    np.save(dir+'/est_C_normalised.npy', est_C_normalised)
else:
    np.save('est_A_normalised.npy', est_A_normalised)
    np.save('est_A_normalised.npy', est_B_normalised)
    np.save('est_A_normalised.npy', est_C_normalised)



    

    

