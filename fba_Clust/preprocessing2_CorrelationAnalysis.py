import argparse
import numpy as np
import preprocessing2_CorrelationAnalysis_functions as cor


parser = argparse.ArgumentParser()
parser.add_argument('path', help= 'Path of directory with .mat files')
parser.add_argument('-avg', action='store_true', help= 'Compute the preprocessing only on the mean .mat files')
parser.add_argument('-out', type=str, help= 'Input(str): directory to save the reduced matrix (by reaction fluxes) of each patients as .mat file')
args = parser.parse_args()


#get the paths of all the .mat files
matDir = args.path
paths = cor.getPaths(matDir)
if args.avg:
    avg = True
else:
    avg = False

print('\nRemove reaction fluxes that are equal to zero')
print('at every solution points and for every patient')
print('-------------------------------------------------')

print('\nGetting the reaction fluxes that are equal to zero at every solution points for each patients...')
index_rfz_allPatients = cor.ReactionEqualtozeroForDifferentPatients(paths, avg)
print('done')


print('\nChecking if those reaction fluxes are the same for every patients ...')
reactionFluxesZ = cor.getReactionEqualtozeroforEveryPatients(index_rfz_allPatients)
print('done')

print('\nCorrelation analysis')
print('-------------------------------------------------')

print('\nGetting the reaction fluxes that can be removed in every single patients...')
rf_to_remove, reactions_to_remove_comparison = cor.correlationAnalysis(paths, reactionFluxesZ, avg)
print('done')

if args.out:
    dir=args.out
else:
    dir='./'

print('\nRemove the correlated reaction fluxes in every patients and save the full reduced matrix (without reaction fluxes equal to zero and the ones that are correlated)...')
cor.removeReactionFluxesCorr(paths, reactionFluxesZ, rf_to_remove, avg, dir)
print('done')