import argparse
import numpy as np
import preprocessingCorr_functions as pp
from scipy.io import savemat


parser = argparse.ArgumentParser()
parser.add_argument('path', help= 'Path of directory with .mat files')
parser.add_argument('-dir', type=str, help= 'Input(str): directory to save the reduced matrix (by reaction fluxes) of each patients as .mat file')
args = parser.parse_args()


#get the paths of all the .mat files
matDir = args.path
paths = pp.getPaths(matDir)
pathsM = pp.getMeanP(paths)

print('\nRemove reaction fluxes that are equal to zero')
print('at every solution points and for every patient')
print('-------------------------------------------------')

print('Getting the reaction fluxes that are equal to zero at every solution points for multiple patients...')
index_rfz_allPatients = pp.ReactionEqualtozeroForDifferentPatients(pathsM)
print('done')

print('Checking if those reaction fluxes are the same in each patients ...')
reactionFluxesZ = pp.getReactionEqualtozeroforEveryPatients(index_rfz_allPatients)
print('done')

print('Removing the reaction fluxes equal to zero at every solution points and for every patient...')
p_reduced_RFZ = pp.removeReactionFluxesZ(pathsM, reactionFluxesZ)
print('done')

print(p_reduced_RFZ['p1'].shape)

print('\nCorrelation analysis')
print('-------------------------------------------------')
print('Getting the reaction fluxes that are removed in every single patients...')
rf_to_remove = pp.correlationAnalysis(p_reduced_RFZ)
print('done')

p_reduced_RF_ZeroAndCorr = pp.removeReactionFluxesCorr(p_reduced_RFZ, rf_to_remove)

print(p_reduced_RF_ZeroAndCorr['p1'].shape)

if args.dir:
    #save each reduced by reaction fluxes patient matrix as .mat file
    for p in p_reduced_RF_ZeroAndCorr.keys():
        savemat(dir+'/p{0}_reducedRF.mat'.format(p), {'mydata': p_reduced_RF_ZeroAndCorr[p]})
        print('patient ',p,' done ')
else:
    # save each reduced by reaction fluxes patient matrix as .mat file
    for p in p_reduced_RF_ZeroAndCorr.keys():
        savemat('p{0}_reducedRF.mat'.format(p), {'mydata': p_reduced_RF_ZeroAndCorr[p]})
        print('patient ', p, ' done ')