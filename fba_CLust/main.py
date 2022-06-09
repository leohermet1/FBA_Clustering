import preProc as pp
import tensorDec as td
import loadNorm as l
import sys 

if len(sys.argv) == 1:
    print(TypeError: main() missing 1 required positional argument: 'argv')

else:
    if len(sys.argv) == 2:
    #get the paths of all the .mat files
    paths = pp.getPaths(sys.argv[1])

    #get only the paths of the .mat files with
    #the solution matrices computed from phenotypes
    #with boudaries compared to the mean of the healthy patients
    pathsM = pp.getMeanP(paths)

    #get the normalized matrices of each patients 
    Nm = pp.getNormM(pathsM)
    print(Nm.shape)

if len(sys.argv) == 3:
    Nm = sys.argv[2]
    l.getNm(Nm)

cp = td.getCPdecomposition(Nm,2)
print(td.getReconstructionError(cp,Nm))

