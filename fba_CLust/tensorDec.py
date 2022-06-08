### imports ###

import tensorly as tl


### tensor decomposition ###

#get the decomposition of a given tensor for n components
def getCPdecomposition(tensor,n):
    cp = tl.decomposition.CP(n)
    cp_tens = cp1.fit_transform(tensor)
    return cp_tens

#get the error between the reconstructed tensor from the decomposition and the original tensor
def getReconstructionError(Dec,originalTensor):
    reconstruction = Dec.to_tensor()
    rec_error = tl.norm(originalTensor - reconstruction)/tl.norm(originalTensor)
    return rec_error
