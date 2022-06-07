import preProc.py

#get the paths of all the .mat files
paths = getPaths('/home/leo/test_data/')

#get only the paths of the .mat files with
#the solution matrices computed from phenotypes
#with boudaries compared to the mean of the healthy patients
pathsM = getMeanP(paths)

#get the normalized matrices of each patients 
norms = getNormM(pathsM)

print(norms.shape)