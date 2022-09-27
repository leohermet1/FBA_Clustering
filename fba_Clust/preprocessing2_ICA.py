import argparse
import numpy as np
import preprocessing2_ICA_functions as ica


parser = argparse.ArgumentParser()
parser.add_argument('path', help= 'Path of directory with .mat files (output of the Euclidian distance function in matlab')
parser.add_argument('-comps', nargs='+', type=int, help= 'Input(list of int): List of the number of components for the ICA')
parser.add_argument('-out', type=str, help= 'Input(str): directory to save the reduced matrix (by reaction fluxes and solution points) of each patients as .npy file')
args = parser.parse_args()


#get the paths of all the .mat files
matDir = args.path
paths = ica.getPaths(matDir)


print('\nSort the solution points of each patient')
print('-------------------------------------------------')

print('Getting the indexes that sort the solution points by their distance to the centric point...')
sorted_indexes = ica.getEucD(paths)
print('done')

print('\nGetting the number of solution points for each patient and their sorted arrays...')
AOS_sorted, sol_dim = ica.getSortedArrOfSol(paths, sorted_indexes)
print('done')

print('\nCropping each patient\'s solution points dimension to the lowest one...')
tensor = ica.getMaxSol(AOS_sorted, sol_dim)
print('done')

print('\nReduce the solution points dimension with ICA')
print('-------------------------------------------------')

print('Getting the centric solution points coordinates...')
centric_sol = ica.getCentricSol(paths)
print('done')

# Initiate list of components
if args.comps:
    componentList = args.comps
else:
    componentList = [*range(2, 76, 1)]
    componentList += [*range(80, 100, 5)]
    componentList += [*range(110, 210, 10)]

# Initiate directory of the output
if args.out:
    dir = args.out
else:
    dir = './'

print('\nReducing the solution points dimension with ICA and sorting the components by their euclidean distances to the previous centric solution point...')
ica.multipleICA(tensor,componentList,centric_sol,dir)
print('done')


