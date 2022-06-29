import argparse, os
import preProc as pp
#import loadNorm as l
#import tensorDec as td


parser = argparse.ArgumentParser()
parser.add_argument('path', help= 'Paste path of directory with .mat files')
parser.add_argument('-tens', help= 'Paste path of .npy file of the pre-processed data')
args = parser.parse_args()


os.chdir(args.path) # to change directory to argument passed for 'path'

# get the paths of all the .mat files
matDir = os.getcwd()
paths = pp.getPaths(matDir)

#Compute scaling and SVD for every patients
nb_components = 100
norms, varExp_MEAN = pp.getNormSVD(paths,nb_components)
print(norms.shape)
print(varExp_MEAN)

#lComp = [1,2]
#rec_error_cp, cp_time, rec_error_par2, par2_time = td.rec_error_cpANDparafac2(Nm,lComp)
#print(rec_error_cp)


