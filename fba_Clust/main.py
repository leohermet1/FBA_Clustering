import argparse
import preprocessing_functions as pp
import numpy as np
import visualization_functions as v


parser = argparse.ArgumentParser()
parser.add_argument('path', help= 'Path of directory with .mat files')
parser.add_argument('-svd', type=int, help= 'nb of component for the SVD')
parser.add_argument('-td', type=int, help= 'nb of component for the tensor decomposition')
parser.add_argument('-npy', nargs="+", type=str, help= '(list) Names of the 3 output as numpy files')
args = parser.parse_args()


# get the paths of all the .mat files
matDir = args.path
paths = pp.getPaths(matDir)

# Compute scaling and SVD for every patients
if args.svd:
    nb_components = args.svd
else:
    nb_components = 100

tensor = pp.getNormSVD(paths, nb_components)

# Compute tensor decomposition on the 3d matrix
if args.td:
    rank = args.td
else:
    rank = 15

est_B_normalised, est_B_normalised, est_C_normalised = pp.tensorDecomposition(tensor, rank)

# Save pre-processed data as numpy file in the current directory
if args.npy:
    namesList = args.npy
    np.save(namesList[0], est_A_normalised)
    np.save(namesList[1], est_B_normalised)
    np.save(namesList[2], est_C_normalised)
else:
    np.save('est_A_normalised.npy', est_A_normalised)
    np.save('est_B_normalised.npy', est_B_normalised)
    np.save('est_C_normalised.npy', est_C_normalised)

# Clustering and visualization

Xt, v1, v2 = v.PCA(est_A_normalised)
v.saveIMG(Xt, v1, v2, 'PCA of the patients', 'PCA_pat.svg')

clusters = v.getCl_K(est_A_normalised, 4)
v.saveIMG(Xt, v1, v2, 'PCA of the patients with computed clusters', 'PCA_pat_compCl.svg', clusters)


    

    

