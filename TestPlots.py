# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 15:17:56 2021

@author: arava
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.interpolate import griddata as gd

file = np.genfromtxt('resist_profile_undercut_28_25_500_-2.5_2.5_0.5_0.5_8.0_8.0_2.0_2.0_1_3.0.csv', delimiter=',')

#file = np.delete(file, np.where(file[:, 2] >= 600), axis=0)
#file = np.delete(file, np.where(file[:, 3] <= 1), axis=0)

x = file[:, 0]
y = file[:, 1]
z = file[:, 2]
disp = file[:, 3]

x_ = x[(z == 50.)]
y_ = x[(z == 50.)]
disp_ = disp[(z == 50.)]

max_x = np.max(x_)
max_y = np.max(y_)

grid_x, grid_y = np.mgrid[0:max_x, 0:max_y]
grid_z0 = gd((x_, y_), disp_, (grid_x, grid_y), method='linear')

fig = plt.figure()
plt.imshow(grid_z0.T, cmap = 'Greens', origin ='lower')
plt.colorbar()
plt.scatter(x,z,s=10,marker='o',color='black')
plt.ylim(20,max_y+5)
plt.title("Displacement field (X)",size =20)
plt.xlabel("X (nm)",size = 16)
plt.ylabel("Z (nm)", size = 16)
plt.savefig("test-disp.png")
plt.show()
plt.close() 

