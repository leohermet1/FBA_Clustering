# FBA_Clustering

## Description
Unveiling mechanisms underlying mortality in Shock Induced Endotheliopathy.

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

Once you know which model(s) you need, with 
```
cd fba_CLust
VarianceWithinHealthyPatients.py
```
You can run,
```
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
cd fba_CLust
VarianceWithinHealthyPatients.py
```
create a folder named reduced_ZeroAndCorr/ and run :
```
python3 preprocessing2_1_Corr.py directoryWithMatlabFiles/ -out reduced_ZeroAndCorr/
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

Directory of the output of the Correlation analysis :
```
-out reduced_ZeroAndCorr/
```
Add the path of the directory where you want to save the output of the Correlation analysis.

### Preprocessing, Euclidean distances :

Create a folder with the name 'reduced_ZeroCorrEuc' (where the outputs needed for the next part (reduced array of solution, euclidean distances of each solutions to the centric point and the coordinates of the centric solution point) will be saved), 
launch MATLAB and run :
```
preprocessing2_EuclideanDistances.m
```
You can also put the path of your folder (previous output) line 1 and 14 (instead of 'reduced_ZeroAndCorr/') and put the path of the folder for each output line 10, 11 and 12.

This script will compute the dense area (around a centric point founded) of the solution point dimension to reduce it.

### Preprocessing, ICA :

Once you have the centric solution, array of solution and euclidean distances (to the centric solution point) for each patients (output of the Euclidean distances script), you can run :

```
python3 preprocessing2_ICA.py reduced_ZeroCorrEuc/
```
You have to enter the paths of the directory where all the mat files of the patients are stored (centric solution, array of solution and euclidean distances).

This script will sort the solution points of each patient by their Euclidean distance to the centric solution point, crop to the lowest dimension to get a tensor, compute ICA and sort the components (feasible solutions) to the centric solution point found previously.

OPTIONS :
```
preprocessing2_ICA.py -h
preprocessing2_ICA.py --help
```

Your list of ICA components :
```
-comps 50 60 70
```

Directory of the output of the ICA :
```
-out directoryOutput/
```
Add the path of the directory where you want to save the tensor(s) with ICA components.

### Preprocessing, Tensor decomposition :

Once you have the ICA tensor(s), you can run :

```
python3 preprocessing2_TensorDecomposition.py directoryWithNumpyFiles/
```

You have to enter the paths of the directory where all the numpy files of the ICA tensors are stored.

This script will compute a tensor decomposition (td) on the ICA tensors with a number of td components equal to the number of ICA components to have the best percentage of data explained by the model.

OPTIONS :
```
preprocessing2_TensorDecomposition.py -h
preprocessing2_TensorDecomposition.py --help
```

Directory of the output of the ICA :
```
-out directoryOutput/
```
Add the path of the directory where you want to save the loss curve and the vectors of the tensor decomposition of each patients as .npy file.




### Visualization :

Once you have preprocessed the data with the first or second method, you can run :

```
python3 visualization.py patientsMatrix/
```

You have to enter the paths of the patients matrix (from the preprocessing run) as .npy file

This script will help to visualize the output of the tensor decomposition by saving the distribution of the patient matrix on 2 components (PCA) in the current directory.

OPTIONS :
```
visualization.py -h
visualization.py --help
```

Compute the sse and silouhette curves :
```
-sse 
```
This option will save the sse and silouhette curves (to find the optimal number of Kmean clusters) in the current directory.

Compute and visualize a number of clusters on the patient matrix :
```
-cl 3
```
This option will save the PCA on 2 components representing the distribution of the patient matrix with a specific number of clusters in the current directory.

Compare the 4 metabolic groups to 4 computed clusters on the patient matrix :
```
-Mgrp
```
This option will save 

  - the PCA on 2 components representing the distribution of the patient matrix with the metabolic groups
   
  - the PCA on 2 components representing the distribution of the patient matrix with the best permutation of the 4 computed clusters
  
  - the distribution of the patients between the best permutation of the computed clusters and the metabolic groups
  
  - the distribution of the patients with identical clusters between the best permutation of the computed ones and the metabolic groups in the current directory.

PCA of the reaction fluxes matrix  :
```
-RF
```
This option will save the PCA on 2 components representing the distribution of the reaction fluxes matrix in the current directory.

PCA of the solution points matrix  :
```
-SP
```
This option will save the PCA on 2 components representing the distribution of the solution points matrix in the current directory.



## Author
Hermet Léo
