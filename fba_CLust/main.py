import preProc as pp
import tensorDec as td
import loadNorm as l
import sys 

if len(sys.argv) == 1:
    #get the paths of all the .mat files
    paths = pp.getPaths('/home/leo/data/')

    #get only the paths of the .mat files with
    #the solution matrices computed from phenotypes
    #with boudaries compared to the mean of the healthy patients
    pathsM = pp.getMeanP(paths)

    #get the normalized matrices of each patients 
    norms = pp.getNormM(pathsM)
    print(norms.shape)

if len(sys.argv) != 1:
    Nm = sys.argv[1]
    l.getNm(Nm)

#cp = td.getCPdecomposition(norms,2)
#print(td.getReconstructionError(cp,norms))

