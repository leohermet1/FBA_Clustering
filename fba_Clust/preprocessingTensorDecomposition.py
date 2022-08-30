import argparse
import numpy as np
import preprocessingTensorDecomposition_functions as td


parser = argparse.ArgumentParser()
parser.add_argument('path', help= 'Path of directory with .mat files (output of the Euclidian distance funciton in matlab')
parser.add_argument('-dir', type=str, help= 'Input(str): directory to save the reduced matrix (by reaction fluxes) of each patients as .mat file')
args = parser.parse_args()


#get the paths of all the .mat files
matDir = args.path
paths = pp.getPaths(matDir)

sorted_indexes, patternID = td.getEucD(paths)

AOS_sorted = td.getSortedArrOfSol(paths, sorted_indexes, patternID)


if args.dir:
    tensor = td.saveTensor(AOS_sorted)
    np.save(dir + '/tensor.npy', tensor)
else:
    tensor = td.saveTensor(AOS_sorted)
    np.save(dir + '/tensor.npy', tensor)