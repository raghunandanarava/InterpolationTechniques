# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 07:50:55 2020

@author: arava
"""


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d
import pandas as pd
#import datacompy
import os


def Compare(dfa, dfb):
    s = pd.Series(['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M'])
    m, n = dfa.shape
    result = pd.DataFrame(columns=s)
    dfb = dfb.to_numpy()
    dfb = dfb.astype('float64')
    match = -1
    
    for i in range(m):
        d = dfa.iloc[i,]
        d = d[s].to_numpy()
        
        d = d.astype('float64')
        d = d.reshape((1, 9))
        
#        print(d.shape)
#        print(dfb.shape)
        
        result = np.isclose(d, dfb, atol = 0.1, equal_nan = True)
#        print(result)
        
        if np.all(result):
            # print('Match found')
            match  = i
            break
#        tmpDf = pd.DataFrame(d, columns = s)
#        tmp = tmpDf.join(dfb, how='inner', lsuffix='_a', rsuffix='_b')
#        lhs = tmp[s + '_a'].values
#        rhs = tmp[s + '_b'].values
#        print(lhs)
#        compare = np.isclose(lhs, rhs, atol=0.002, rtol=0)
#        result[i, :] = pd.DataFrame(compare, columns=s, index=tmp.index)
#    
#    print(result)
    return match

files_data = pd.read_csv('DesignPointsFile1.csv', sep=r'\s*,\s*')

ax = plt.axes(projection='3d')
data = np.load('resist_profile-new.npy')

x = np.asarray(data[:, 0])
y = np.asarray(data[:, 1])
z = np.asarray(data[:, 2])

y_min = np.amin(y)
x_new = x[(y == y_min)]
z_new = z[(y == y_min)]
z_min = np.amin(z_new)
z_max = np.amax(z_new)
#H = z_max - z_min

dimensions = np.zeros((1, 9))
dimensions[0, 1] = dimensions[0, 3] = dimensions[0, 5] = dimensions[0, 7] = (40 / 4) * 1e-3
for i in range(0, 9, 2):
    x_min = np.amin(x_new[(z_new == z_min)])
    x_max = np.amax(x_new[(z_new == z_min)])
    dimensions[0, i] = (x_max - x_min) * 1e-3
    z_min = round(z_min + 8.75)

temp = dimensions[0, 7]
dimensions[0, 7] = dimensions[0, 8]
dimensions[0, 8] = temp

dimensionSet = pd.DataFrame(data = dimensions, columns = ['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M'])
print(dimensionSet)

c = Compare(files_data, dimensionSet)
print(c)

y_next = y_min + 1
x_next = x[(y == y_next)]
z_next = z[(y == y_next)]
z_min_next = np.amin(z_next)
z_max_next = np.amax(z_next)

print(np.min(x_next[(z_next == z_min_next)]))


#temp_string = 'DP_' + str(c)
#required_files = []
#
#for file in os.listdir('K:\litho-stud-win\Arava\Simulations\FinalSimulations\displacement-field'):
#    if file.startswith(temp_string):
#        required_files.append(file)
#        break
#
#disp = []
#
#for files in required_files:
#    disp.append(np.genfromtxt(files, delimiter=','), axis=0)
#
#disp[:, 1:6] = disp[:, 1:6] * 1000
#xz = disp[:,1:3]
#x = disp[:,1]
#z = disp[:,2]
#disp_x = disp[:,4]
#max_x = np.max(disp[:,1])
#max_y = np.max(disp[:,2])
#grid_x, grid_y = np.mgrid[0:max_x, 0:max_y]
#grid_z0 = gd(xz, disp_x, (grid_x, grid_y), method='cubic')

#df3 = pd.merge(files_data, dimensionSet, left_on = ['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M'], right_on = ['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M'])
#print(df3)

#compare = datacompy.Compare(files_data, dimensionSet, rel_tol = 0.002, on_index=True)
#print(compare.report())
#print(compare.intersect_rows)

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111)
ax.scatter(x_next, z_next)
plt.show

