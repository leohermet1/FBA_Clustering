import argparse
import numpy as np
import preprocessing2_TensorDecomposition_functions as td

parser = argparse.ArgumentParser()
parser.add_argument('path', help= 'Path of directory with .mat files (output of the Euclidian distance function in matlab')
parser.add_argument('-comps', nargs='+', type=int, help= 'Input(list of int): List of the number of components for the ICA')
parser.add_argument('-out', type=str, help= 'Input(str): directory to save the loss curve and the vectors of the tensor decomposition of each patients as .npy file')
args = parser.parse_args()

#get the paths of all the .mat files
npyDir = args.path
paths = td.getPaths(npyDir)

# Initiate directory of the output
if args.out:
    dir = args.out
else:
    dir = './'

# Initiate the list of ICA tensor(s) to compute (here it is the 50 tensors of 20 to 70 ICA components)
ICA_list = [*range(20, 71, 1)]
print(ICA_list)
# Tensor decomposition on each numpy file (different ICA components
td.multipleTensorDecomposition(paths,dir,ICA_list)