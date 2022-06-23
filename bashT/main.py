import fileinput
import preProc as pp
import loadNorm as l
import tensorDec as td

i=0
for line in fileinput.input(files='input.in'):
    if i==0:
        numpyPath = line
    i += 1

Nm = l.getNm(numpyPath)

lComp = [1,2]
rec_error_cp, cp_time, rec_error_par2, par2_time = td.rec_error_cpANDparafac2(Nm,lComp)
print(rec_error_cp)


