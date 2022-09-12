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

#### Run
### First method :
## Preprocessing :
```
cd fba_CLust
python3 preprocessing1_SVDandTensorDecomposition.py directoryWithMatlabFiles/
```
You have to enter the paths of the directory where all the mat files of the patients are stored
# Options :
```
preprocessing1_SVDandTensorDecomposition.py -h
preprocessing1_SVDandTensorDecomposition.py -help
```
Visualize the impact of the variance within the healthy patients :
```
-mimema dir/
```
This option will save the distribution of the solution points for each patients as .svg files (search for 3 distinct groups represented by the min, mean and max matrices to see if we need all 3 models)
Add the path of the directory where you want to save the .svg files

Compute only on the mean.mat files :
```
-avg
```

Number of SVD components :
```
-svd 350
```
(default = 10)

Number of TensorDecomposition components :
```
-td 350
```
(default = 10)

Directory of the output of the tensor decomposition :
```
-npy directoryOutput/
```
Add the path of the directory where you want to save the output of the tensor decomposition


Visualization :



## Author
Hermet Léo
