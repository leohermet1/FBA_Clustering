import questions as q
import preProc as pp
import loadNorm as l
import tensorDec as td


bool = q.npyQuestion()

if bool:
    Nm = q.npyPath()
    l.getNm(Nm)

else:
    matDir = q.matPath()

    # get the paths of all the .mat files
    paths = pp.getPaths(matDir)

    # get only the paths of the .mat files with
    # the solution matrices computed from phenotypes
    # with boudaries compared to the mean of the healthy patients
    pathsM = pp.getMeanP(paths)

    # get the normalized matrices of each patients
    Nm = pp.getNormM(pathsM)
    print(Nm.shape)

cp = td.getCPdecomposition(Nm,2)
print(td.getReconstructionError(cp,Nm))


