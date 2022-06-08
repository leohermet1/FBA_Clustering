import scipy.io as spio

#load the matlab structure
mean10 = spio.loadmat('/home/leo/test_data/modelPatient_Sampled_10_Mean.mat')

#get the structure array
sample10mean = mean10['sampleMetaOutC']
print(sample10mean.dtype)
