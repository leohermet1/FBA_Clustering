import questions as q
import preProc as pp
import loadNorm as l
import tensorDec as td


boolNPY = q.npyQuestion()

if boolNPY:
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

    boolSVD = q.SVDquestion()
    if boolSVD:
        nb_components = q.nbComp()
        Nm = pp.getSVD(pathsM,nb_components)
        print(Nm.shape)
    else:
        # get the normalized matrices of each patients
        Nm = pp.getNormM(pathsM)
        print(Nm.shape)

lComp = [1]
rec_error_cp, cp_time, rec_error_par2, par2_time = td.rec_error_cpANDparafac2(Nm,lComp)
print(rec_error_cp)


