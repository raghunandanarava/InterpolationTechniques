# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 13:21:37 2021

@author: arava
"""

import os
import numpy as np
import pdb

def getDesignPointFile(inversed, youngsModulus):
    cwd = os.getcwd()
    cwd = cwd + '/DesignPoints'
    os.chdir(cwd)
    
    newList = None
    
    if inversed:
        fileEnding = 'Reverse_0' +  str(int(youngsModulus * 10)) + '.csv'
    else:
        fileEnding = '_0' + str(int(youngsModulus * 10)) + '.csv'
    
    items = os.listdir()
    newList = [name for name in items if name.endswith(fileEnding)]
    # for name in items:
    #     if name.endswith(fileEnding):
    #         newList = name
    #         break
    
    designPoints = np.genfromtxt(newList, delimiter=',')
    
    return designPoints

def getFields(matchNumber, inversed, youngsModulus):
    # cwd = os.getcwd()
    # cwd = cwd + '/AssymetricSimulations'
    # os.chdir(cwd)
    os.chdir('../AssymetricSimulations')
    newList = None
    fileName = None
    #pdb.set_trace()
    if inversed:
        dirEnding = 'Overcut_0' + str(int(youngsModulus * 10))
    else:
        dirEnding = 'Undercut_0' + str(int(youngsModulus * 10))
    
    items = os.listdir()
    newList = [name for name in items if name.endswith(dirEnding)]
    # for name in items:
    #     if name.endswith(dirEnding):
    #         newList = name
    #         break
    # print(newList)
    os.chdir(str(newList[0]) + '/displacement-field')

    files = os.listdir()
    fileName = [file for file in files if file.startswith('DP_' + str(int(matchNumber[0])) + '_')]

    
    # for field in fields:
    #     # newCwd = cwd + '/' + field
    #     # os.chdir(newCwd)
    #     os.chdir(field)
    #     files = os.listdir()
    #     if fileName.size == 0:
    #         fileName = np.array([file for file in files if file.startswith('DP_' + str(matchNumber) + '_')])
    #     else:
    #         fileName = np.vstack((fileName, np.array([file for file in files if file.startswith('DP_' + str(matchNumber) + '_')])))
    #     os.chdir('..')
    #     # for file in files:
    #     #     if file.startswith('DP_' + matchNumber):
    #     #         fileName = file
    # fileName = np.reshape(fileName, (1, fileName.size))
    
    #pdb.set_trace()
    displacementField = np.genfromtxt(str(fileName[0]), delimiter=',')
    # os.chdir(cwd + '/elastic-strain-field')
    # elasticStrainField = np.genfromtxt(str(fileName[0][1]), delimiter=',')
    # os.chdir(cwd + '/plastic-strain-field')
    # plasticStrainField = np.genfromtxt(str(fileName[0][2]), delimiter=',')
    # os.chdir(cwd + '/total-strain-field')
    # totalStrainField = np.genfromtxt(str(fileName[0][3]), delimiter=',')
    
    displacementField = displacementField[:, 1:5] * 1000
    # max_height_coordinate = np.max(displacementField[:, 2])
    # min_height_coordinate = np.min(displacementField[:, 2])
    
    # newCoordinate = max_height_coordinate - (0.1 * (max_height_coordinate - min_height_coordinate))
    # displacementField = np.delete(displacementField, np.where(displacementField[:, 2] < newCoordinate), axis=0)
    
    os.chdir('../../../InterpolationTechniques-1')
    
    return displacementField