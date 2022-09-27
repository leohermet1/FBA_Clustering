import argparse
import VarianceWithinHealthyPatients_functions  as f
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('path', help= 'Path of directory with .mat files')
parser.add_argument('-out', type=str, help= 'Input(str): Path of the directory where you want to save the .svg files'
                                     '\nVisualize the impact of the variance within the healthy patients'
                                     '\nThis option will save the distribution of the solution points for each patients as .svg files '
                                     '\n(search for 3 distinct groups represented by the min, mean and max matrices to see if we need all 3 models)')
args = parser.parse_args()


# get the paths of all the .mat files
matDir = args.path
paths = f.getPaths(matDir)

# Visualize the impact of the variance within the healthy patients
# It will save the distribution of the solution points for each patients as .svg files
if args.out:
    dir = args.out
    f.norm3models(paths, dir)
else:
    dir = './'
    f.norm3models(paths, dir)