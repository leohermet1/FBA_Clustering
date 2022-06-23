import preProc as pp
import loadNorm as l
import tensorDec as td


Nm = l.getNm('/zhome/5e/6/176978/Desktop/FBA_Clustering/bashT/test_data/tensor95.npy')

lComp = [2,4,10,20,40,80]
rec_error_cp, cp_time, rec_error_par2, par2_time = td.rec_error_cpANDparafac2(Nm,lComp)
print('rec_error_cp: ',rec_error_cp,
      '\ncp_time: ',cp_time,
      '\nrec_error_par2: ', rec_error_par2,
      '\npar2_time: ', par2_time)


