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
+ `pip3 install sklearn`
+ `pip3 install pandas`
+ `pip3 install tensorly`

+ `Statistics and Machine Learning Toolbox`

## Run
### FIRST METHOD :
#### Preprocessing :
```
cd fba_CLust
python3 preprocessing1_SVDandTensorDecomposition.py directoryWithMatlabFiles/
```
###### You have to enter the paths of the directory where all the mat files of the patients are stored
##### OPTIONS :
```
preprocessing1_SVDandTensorDecomposition.py -h
preprocessing1_SVDandTensorDecomposition.py -help
```
##### Visualize the impact of the variance within the healthy patients :
```
-mimema dir/
```
###### _This option will save the distribution of the solution points for each patients as .svg files (search for 3 distinct groups represented by the min, mean and max matrices to see if we need all 3 models)_
###### _Add the path of the directory where you want to save the .svg files_

##### Compute only on the mean.mat files :
```
-avg
```

##### Number of SVD components (default = 10) :
```
-svd 350
```

##### Number of TensorDecomposition components (default = 10) :
```
-td 350
```

##### Directory of the output of the tensor decomposition :
```
-npy directoryOutput/
```
###### _Add the path of the directory where you want to save the output of the tensor decomposition_


Visualization :



## Author
Hermet Léo
