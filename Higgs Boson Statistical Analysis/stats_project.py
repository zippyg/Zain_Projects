# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 22:57:18 2023

@author: Matthew Howarth
"""
#%% Import 
import numpy as np
import matplotlib.pyplot as plt
import STOM_higgs_tools
from tqdm.notebook import tqdm
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit
from scipy.stats import chi2
#%%
vals = STOM_higgs_tools.generate_data()
nbins=30
mass_range=[104,155]

bin_heights, bin_edges, patches = plt.hist(vals, range = mass_range, bins = nbins,color='pink')
bin_centre = bin_edges+0.5*(bin_edges[1]-bin_edges[0])
plt.errorbar(bin_centre[0:30],bin_heights,yerr=np.sqrt(bin_heights),capsize=2,fmt='x',ms=2,ecolor='black')
plt.show() 
#%%
L=100#number of A and lambda values to check
A=np.linspace(5e4,6e4,L) #range of predicted A values
lamb=np.linspace(20,40,L) #range of predicted lambda values
pbar = tqdm(range(L))
chi_grid=np.full((L,L),1e6)
mass_range_low=[104,120]
nbins_low=9
for i in range(L):
    pbar.update(1)
    for j in range(L):
        chi=STOM_higgs_tools.get_B_chi(vals,mass_range_low,nbins_low,A[i],lamb[j])
        chi_grid[i,j]=chi
min_index = np.unravel_index(np.argmin(chi_grid), chi_grid.shape)
chi_min = chi_grid[min_index[0],min_index[1]]
A_opt_b = A[min_index[0]]
lamb_opt_b = lamb[min_index[1]]
print(f'lambda = {lamb_opt_b}, A = {A_opt_b}, minimum chi={chi_min}')
