import os
from natsort import os_sorted

import re

import numpy as np
import matplotlib.pyplot as plt

import tensorly as tl
from tensorly.decomposition import parafac2
import numpy.linalg as la



### Get the paths ###

#definition of the function that get all the paths of the .mat files
def getPaths(directory):
    p = []
    #browse every files in the directory
    for filename in os.listdir(directory):
        #only get the files that ends by '.npy'
        if filename.endswith(".npy") :
            p.append(os.path.join(directory, filename))
            continue
        else:
            continue
    paths = os_sorted(p)

    return paths



### Tensor decomposition ###

def td(tensor, rank):
    print(f'Number of components: {rank}')
    print('\nNormal dataset')
    print('-------------------------------------------')
    best_err = np.inf
    decomposition = None

    # Initialise and fit 5 models
    for run in range(5):
        print(f'Training model {run}...')
        trial_decomposition, trial_errs = parafac2(tensor, rank, return_errors=True, tol=1e-8, n_iter_max=80,
                                                   random_state=run)
        print(f'Number of iterations: {len(trial_errs)}')
        print(f'Final error: {trial_errs[-1]}')
        # Chose the model with the lowest error in order to avoid local minima
        if best_err > trial_errs[-1]:
            best_err = trial_errs[-1]
            err = trial_errs
            decomposition = trial_decomposition
        print('-------------------------------')
    print('\n')
    print(f'Best model error: {best_err}')
    
    # compute the reconstruction error
    est_tensor = tl.parafac2_tensor.parafac2_to_tensor(decomposition)
    est_weights, (est_A, est_B, est_C) = tl.parafac2_tensor.apply_parafac2_projections(decomposition)

    reconstruction_error = la.norm(est_tensor - tensor)
    recovery_rate = 1 - reconstruction_error / la.norm(tensor)

    print(f'{recovery_rate:2.0%} of the data is explained by the model')
    print('\n')

    # get the matrices that represent each dimensions
    est_A, est_projected_Bs, est_C = tl.parafac2_tensor.apply_parafac2_projections(decomposition)[1]

    sign = np.sign(est_A)
    est_A = np.abs(est_A)
    est_projected_B = sign[:, np.newaxis] * est_projected_Bs

    est_A_normalised = est_A / la.norm(est_A, axis=0)
    est_Bs_normalised = [est_B / la.norm(est_B, axis=0) for est_B in est_projected_Bs]
    est_B_normalised = est_Bs_normalised[0]
    est_C_normalised = est_C / la.norm(est_C, axis=0)

    return (est_A_normalised, est_B_normalised, est_C_normalised, err)

def multipleTensorDecomposition(paths,dir):
    for p in paths:
        tensor = np.load(p)
        ICA_comp = re.search(r'\d+', p).group()
        print(f'\n{ICA_comp} ICA components')
        print('--------------------------------------------------------------')
        rank = int(ICA_comp)

        # Tensor decomposition
        est_A_normalised_ICA, est_B_normalised_ICA, est_C_normalised_ICA, err = td(tensor, rank)

        # Saving the loss curve as .svg file to see if it converges
        loss_fig, loss_ax = plt.subplots(figsize=(9, 9 / 1.6))
        loss_ax.plot(range(1, len(err)), err[1:])
        loss_ax.set_xlabel('Iteration number')
        loss_ax.set_ylabel('Relative reconstruction error')
        mathematical_expression_of_loss = r"$\frac{\left|\left|\hat{\mathcal{X}}\right|\right|_F}{\left|\left|\mathcal{X}\right|\right|_F}$"
        loss_ax.set_title(f'Loss plot: {mathematical_expression_of_loss} \n (starting after first iteration)', fontsize=16)
        xticks = loss_ax.get_xticks()
        loss_ax.set_xticks([1] + list(xticks[1:]))
        loss_ax.set_xlim(1, len(err))
        plt.tight_layout()
        plt.savefig(dir + "/LossCurve_{0}ICAcomponents.svg".format(ICA_comp),
                    format="svg")

        # Saving the matrices decomposition of each dimension
        np.save(dir + "/patientsMatrix_{0}ICAcomponents.npy".format(ICA_comp), est_A_normalised_ICA)
        np.save(dir + "/reactionFluxesMatrix_{0}ICAcomponents.npy".format(ICA_comp), est_B_normalised_ICA)
        np.save(dir + "/solutionPointsMatrix_{0}ICAcomponents.npy".format(ICA_comp), est_C_normalised_ICA)

