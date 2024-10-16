'''
This is an example of computing the Likeness Score: LS on datasets of real images and generated images by GANs.
It includes codes to compute the *2-class* distance-based separability index (DSI). There are two versions (CPU and GPU) of DSI.

Inputs:             Two folders have real images and generated images

Related paper:      A Novel Measure to Evaluate Generative Adversarial Networks Based on Direct Analysis of Generated Images
                    Neural Computing and Applications, 2021
                    https://doi.org/10.1007/s00521-021-06031-5
                    
By:                 Shuyue Guan
                    https://shuyueg.github.io/
'''

import glob
import numpy as np
import scipy.misc
from scipy.spatial.distance import minkowski
from scipy.stats import ks_2samp
import time,imageio, os
import torch

# input images
def get_image_vector(filename):
    im = imageio.imread(filename, pilmode = 'RGB')
    
    return np.float32(np.ndarray.flatten(im))/255


#####################  LS CPU ver. ##################{

def dists(data):  # compute ICD
    num = data.shape[0]
    data = data.reshape((num, -1))
    dist = []
    for i in tqdm(range(0,num-1)):
        for j in range(i+1,num):
            dist.append(minkowski(data[i],data[j]))
            
    return np.array(dist)

def dist_btw(a,b):  # compute BCD
    a = a.reshape((a.shape[0], -1))
    b = b.reshape((b.shape[0], -1))
    dist = []
    for i in tqdm(range(a.shape[0])):
        for j in range(b.shape[0]):
            dist.append(minkowski(a[i],b[j]))
            
    return np.array(dist)


def LS(real,gen):  # KS distance btw ICD and BCD
    dist_real = dists(real)  # ICD 1
    dist_gen = dists(gen)  # ICD 2
    distbtw = dist_btw(real, gen)  # BCD
    
    D_Sep_1, _ = ks_2samp(dist_real, distbtw)
    D_Sep_2, _ = ks_2samp(dist_gen, distbtw)

    return 1- np.max([D_Sep_1, D_Sep_2])  # LS=1-DSI

#####################################################}

#####################  LS GPU ver. ##################{
# To compute Euclidean distances by torch tensors

def gpu_LS(real,gen):
    # to torch tensors
    t_gen = torch.from_numpy(gen)
    t_real = torch.from_numpy(real)

    dist_real = torch.cdist(t_real, t_real)  # ICD 1
    dist_real = torch.flatten(torch.tril(dist_real, diagonal=-1))  # remove repeats
    dist_real = dist_real[dist_real.nonzero()].flatten()  # remove distance=0 for distances btw same data points

    dist_gen = torch.cdist(t_gen, t_gen)  # ICD 2
    dist_gen = torch.flatten(torch.tril(dist_gen, diagonal=-1))  # remove repeats
    dist_gen = dist_gen[dist_gen.nonzero()].flatten()  # remove distance=0 for distances btw same data points

    distbtw = torch.cdist(t_gen, t_real)  # BCD
    distbtw = torch.flatten(distbtw)

    D_Sep_1, _ = ks_2samp(dist_real, distbtw)
    D_Sep_2, _ = ks_2samp(dist_gen, distbtw)

    return 1- np.max([D_Sep_1, D_Sep_2])  # LS=1-DSI

#####################################################}

if __name__ == '__main__':

    AbsLoc = r'D:\datasets'

    filenames_1 = glob.glob(os.path.join(AbsLoc, 'generated/*.png'))
    gen = np.array([get_image_vector(filename) for filename in filenames_1])

    filenames_2 = glob.glob(os.path.join(AbsLoc, 'real/*.png'))
    real = np.array([get_image_vector(filename) for filename in filenames_2])

    print('real #:   '+str(len(real)))
    print('gen #:   '+str(len(gen)))

    print('\n', 'LS= ', LS(real, gen))  # CPU ver.
    print('\n', 'LS= ', gpu_LS(real, gen))  # GPU ver.

    
    
    
    
