### imports ###

from tensorly.decomposition import CP
from tensorly.decomposition import parafac2
import tensorly as tl

import time

import matplotlib.pyplot as plt

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

    perc = 100
    perc_rec_error_cp = [x * perc for x in rec_error_cp]
    perc_rec_error_par2 = [x * perc for x in rec_error_par2]

    # Plot a simple line chart
    plt.plot(lComp, perc_rec_error_cp, label="CP reconstruction error")

    # Plot another line on the same chart/graph
    plt.plot(lComp, perc_rec_error_par2, label="Parafac2 reconstruction error")

    plt.ylabel('% of reconstruction error')
    plt.xlabel('number of components')
    plt.title('Reconstruction error')
    plt.legend()
    plt.show()



