### imports ###

from tensorly.decomposition import CP
from tensorly.decomposition import parafac2
import tensorly as tl
import time

### tensor decomposition ###

def compute_reconstruction_err(tensor, reconstruction):
    rec_error = tl.norm(tensor - reconstruction) / tl.norm(tensor)
    return rec_error


def rec_error_cpANDparafac2(tensor, lComp):
    # init list of reconstruction error for each component
    rec_error_cp = []
    rec_error_par2 = []
    cp_time = []
    par2_time = []

    for c in lComp:
        # cp decomposition
        start = time.time()

        cp = CP(c)
        cp_tens = cp.fit_transform(tensor)
        cp_reconstruction = cp_tens.to_tensor()
        rec_error_cp.append(compute_reconstruction_err(tensor, cp_reconstruction))

        end = time.time()
        cp_time.append(round(end - start, 2))

        # parafac2 decomposition
        start = time.time()

        par = parafac2(tensor, c)
        par2_reconstruction = par.to_tensor()
        rec_error_par2.append(compute_reconstruction_err(tensor, par2_reconstruction))

        end = time.time()
        par2_time.append(round(end - start, 2))

        print('decomposition for', c, 'components done.')

    return rec_error_cp, cp_time, rec_error_par2, par2_time