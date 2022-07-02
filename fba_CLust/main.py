import argparse, os
import preProc as pp
import numpy as np
import clust as cl


parser = argparse.ArgumentParser()
parser.add_argument('path', help= 'Paste path of directory with .mat files or directly the path of the .npy file of the pre-processed data')
parser.add_argument('-svd', type=int, help= 'nb of component for the SVD')
parser.add_argument('-td', type=int, help= 'nb of component for the tensor decomposition')
parser.add_argument('-cl', nargs="+", type=int, help= 'list of clusters')
args = parser.parse_args()

isDirectory = os.path.isdir(args.path)

if isDirectory:
    # get the paths of all the .mat files
    matDir = args.path
    paths = pp.getPaths(matDir)

    # Compute scaling and SVD for every patients
    if args.svd:
        nb_components = args.svd
        tensor, varExp_MEAN = pp.getNormSVD(paths, nb_components)
        print('average explained variance for SVD: ', round(varExp_MEAN, 3), '%')
    else:
        nb_components = 100
        tensor, varExp_MEAN = pp.getNormSVD(paths,nb_components)
        print('average explained variance for SVD: ',round(varExp_MEAN,3),'%')

    # Compute tensor decomposition on the 3d matrix
    if args.td:
        nb_components = args.td
        patVectors = pp.tensorDecomposition(tensor, nb_components)
    else:
        nb_components = 15
        patVectors = pp.tensorDecomposition(tensor, nb_components)

    # Save pre-processed data as numpy file in the current directory
    np.save('ppData.npy',patVectors)

    # CLustering
    # Xt = cl.PCA_sol(patVectors)
    # cl.computeK(patVectors, 15)
    # 
    # if args.cl:
    #     clList = args.cl
    #     cl.visClMeths(Xt, clList, patVectors)
    # else:
    #     clList = [4,6]
    #     cl.visClMeths(Xt, clList, patVectors)
    

else:
    # Load pre-processed data (numpy file) with the given path
    patVectors = np.load(args.path)
    
    # CLustering
    Xt = cl.PCA_sol(patVectors)
    cl.computeK(patVectors, 15)
    
    if args.cl:
        clList = args.cl
        cl.visClMeths(Xt, clList, patVectors)
    else:
        clList = [4,6]
        cl.visClMeths(Xt, clList, patVectors)
    

