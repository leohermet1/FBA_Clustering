import argparse
import visualization_functions as v


parser = argparse.ArgumentParser()
parser.add_argument('path', help= 'Path of directory with the .npy files from the preprocessing run')
parser.add_argument('-svd', type=int, help= 'nb of component for the SVD')
parser.add_argument('-td', type=int, help= 'nb of component for the tensor decomposition')
parser.add_argument('-npy', nargs="+", type=str, help= '(list) Names of the 3 output as numpy files')
args = parser.parse_args()

# Clustering and visualization

Xt, v1, v2 = cl.PCA(est_A_normalised)
cl.saveIMG(Xt, v1, v2, 'PCA of the patients', image_name)
cl.computeK(patVectors, 15)

if args.cl:
    clList = args.cl
    cl.visClMeths(Xt, clList, patVectors)
else:
    clList = [4,6]
    cl.visClMeths(Xt, clList, patVectors)