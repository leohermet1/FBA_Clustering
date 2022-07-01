import argparse, os
import preProc as pp
import numpy as np
#import loadNorm as l


parser = argparse.ArgumentParser()
parser.add_argument('path', help= 'Paste path of directory with .mat files or directly the path of the .npy file of the pre-processed data')
parser.add_argument('-svd', type=int, help= 'nb of component for the SVD')
parser.add_argument('-td', help= 'nb of component for the tensor decomposition')
args = parser.parse_args()

isDirectory = os.path.isdir(args.path)

if isDirectory:
    # get the paths of all the .mat files
    matDir = args.path
    paths = pp.getPaths(matDir)

    # Compute scaling and SVD for every patients
    if args.svd:
        nb_components = args.svd
        norms, varExp_MEAN = pp.getNormSVD(paths, nb_components)
        print(norms.shape)
        print(varExp_MEAN)
    else:
        nb_components = 100
        norms, varExp_MEAN = pp.getNormSVD(paths,nb_components)
        print(norms.shape)
        print(varExp_MEAN)

    # lComp = [1,2]
    # rec_error_cp, cp_time, rec_error_par2, par2_time = td.rec_error_cpANDparafac2(Nm,lComp)
    # print(rec_error_cp)

else:
    Nm = np.load(args.path)
    lComp = [1,2]
    rec_error_par2, par2_time = pp.rec_error_cpANDparafac2(Nm,lComp)

