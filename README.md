# FBA_Clustering

## Description
This package compute and display the clusters that can be found between multiple patients matrices obtained by FBA (reaction-solution matrices).

## Version
1.0.0

## Installation
Before trying to run this software 
```
git clone https://github.com/leohermet1/FBA_Clustering.git
```

### DEPENDENCIES:
You can use the virtual environnement :
```
source venv_1/Scripts/activate
```
or install every dependencies :
+ `pip3 install natsort`
+ `pip3 install numpy`
+ `pip3 install scipy`
+ `pip3 install matplotlib`
+ `pip3 install sklearn`
+ `pip3 install pandas`
+ `pip3 install tensorly`

+ `Statistics and Machine Learning Toolbox`

## RUN

### Visualize the impact of the variance within the healthy patients :
First script to run that checks if we need to consider the variability within the control group.

It will save the distribution of the solution points for each patients as .svg files (search for 3 distinct groups represented by the min, mean and max matrices to see if we need all 3 models).
```
cd fba_CLust
python3 VarianceWithinHealthyPatients.py directoryWithMatlabFiles/
```
You have to enter the paths of the directory where all the mat files of the patients are stored.

OPTIONS :
```
VarianceWithinHealthyPatients.py -h
VarianceWithinHealthyPatients.py --help
```
Path of the output :
```
-out dir/
```
Add the path of the directory where you want to save the .svg files.

### FIRST METHOD :
### Preprocessing :
```
cd fba_CLust
python3 preprocessing1_SVDandTensorDecomposition.py directoryWithMatlabFiles/
```
You have to enter the paths of the directory where all the mat files of the patients are stored.

OPTIONS :
```
preprocessing1_SVDandTensorDecomposition.py -h
preprocessing1_SVDandTensorDecomposition.py --help
```

Compute only on the mean.mat files :
```
-avg
```

Number of SVD components (default = 10) :
```
-svd 350
```

Number of TensorDecomposition components (default = 10) :
```
-td 350
```

Directory of the output of the tensor decomposition :
```
-npy directoryOutput/
```
Add the path of the directory where you want to save the output of the tensor decomposition.


### SECOND METHOD :
### Preprocessing, Correlation analysis :
First script of the second method.
Once you know which model(s) you need, with 
```
VarianceWithinHealthyPatients.py
```
You can run :
```
cd fba_CLust
python3 preprocessing2_1_Corr.py directoryWithMatlabFiles/
```
You have to enter the paths of the directory where all the mat files of the patients are stored.

This script will delete the reaction fluxes equal to zero at every solution points for every patients and the reaction fluxes that are correlated to each others.

OPTIONS :
```
preprocessing2_Corr.py -h
preprocessing2_Corr.py --help
```

Compute only on the mean.mat files :
```
-avg
```

Directory of the output of the tensor decomposition :
```
-out directoryOutput/
```
Add the path of the directory where you want to save the output of the tensor decomposition.

### Preprocessing, Euclidean distances :
Put all the MATLAB files (output of the previous script) in a folder named 'reduced_ZeroAndCorr', create a folder with the name 'reduced_ZeroCorrEuc' (where the outputs needed for the next part (reduced array of solution, euclidean distances of each solutions to the centric point and the coordinates of the centric solution point) will be saved), launch MATLAB and run :
```
preprocessing2_EuclideanDistances.m
```
You can also put the path of your folder (previous output) line 1 and 14 (instead of 'reduced_ZeroAndCorr/') and put the path of the folder for each output line 10, 11 and 12.

### Preprocessing, Tensor decomposition :



Visualization :



## Author
Hermet Léo
