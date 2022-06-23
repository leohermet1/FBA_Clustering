import numpy as np

def getNm(Nm):
    data = np.load(Nm)
    print(data.shape)
    print(type(data))
