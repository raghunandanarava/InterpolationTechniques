# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 10:18:09 2021

@author: arava
"""

from tokenize import Name
from zipfile import ZIP_FILECOUNT_LIMIT
import numpy as np
import os
from CompareAndInterpolate import *
from RefactorDesignPoints import *
from DimensionsExtraction import *
from GetDesignPointsFile import *
from InterpolationAtEnds import *
import pdb
import h5py
import copy
# import open3d as o3d


"""Young's modulus is defined here"""
youngsModulus = 0.3

"""Rough Profiles names are obtained"""
roughProfiles = os.listdir('../Rough-Profiles-1')

"""The data points are obtained and refactored"""
#pdb.set_trace()
dataPoints = np.genfromtxt('../DesignPoints/Undercut.csv',
                           delimiter=',')
refactorise = Refactorisation(dataPoints)
refactoredPoints = refactorise.refactor()

collapse = []
data_all = np.zeros((len(roughProfiles), 1), dtype='object')

f = h5py.File("train.h5", "w", libver='latest')

"""Looping over the profiles"""
for ii, profile in enumerate(roughProfiles):
    """The profile name, pitch, and height are extracted here"""
    profileName = str(profile).split('.npy')[0]
    nothing = str(profile).split('_')
    pitch = float(nothing[3])
    height = float(nothing[4])
    length = float(str(nothing[5]))
    # xLen = float(nothing[15])
    # zLen = float(nothing[16])
    # yLen = float(nothing[17].split('.')[0])

    totalData = np.array([])
    
    """Point cloud is obtained"""
    data = np.load('../Rough-Profiles-1/' + str(profile))
    x = np.array(data[:, 0])
    z = np.array(data[:, 1])
    y = np.array(data[:, 2])
    z_min = np.min(z)
    z_max = np.max(z)

    # xMesh, yMesh = np.mgrid[x_min : x_max : (pitch * 1j), y_min : y_max : (height * 1j)]
    # xMesh, yMesh = xMesh.flatten(), yMesh.flatten()
    
    """From the refactored points, extract only that match the pitch and
    height of the profile"""
    rowMask = (np.expand_dims(refactoredPoints[:, 15], axis=1)  == pitch * 1e-3).all(axis=1)
    profilePoints = refactoredPoints[rowMask, :]
    
    """Mask for the lengths"""
    # rowMask = (np.expand_dims(profilePoints[:, 16], axis=1) == round(length * 1e-3, 3)).all(axis=1)
    # profilePoints = profilePoints[rowMask, :]

    """Quick fix for heights 0.025 nm"""
    heightsFromPoints = profilePoints[:, 11] + profilePoints[:, 12] + profilePoints[:, 13] + profilePoints[:, 14]
    heightsFromPoints = np.where(heightsFromPoints == 0.0248, 0.025,
                                 heightsFromPoints)
    heightsFromPoints = np.where(heightsFromPoints == 0.0352, 0.035, heightsFromPoints)
    
    rowMask = (np.expand_dims(heightsFromPoints, axis=1) == height * 1e-3).all(axis=1)
    profilePoints = profilePoints[rowMask, :]
    
    """Several arrays required are initialised here"""
    dimensions = np.zeros((2, 14))
    matches = np.zeros((2, 1))
    increments = np.zeros((2, 1))
    inversions = np.zeros((2, 1))
    # xForInt = np.array([])
    # yForInt = np.array([])
    # zForInt = np.array([])
    maxDis = []
    lowestWidth = []
    extrapolateAtStart = False
    temporaryNumber = 0.
    
    """Looping over the cross-sections of the profile"""
    for i, z_value in enumerate(range(z_min, z_max + 1, 1)):
        """Extracting the planar point cloud"""
        xs, ys, yMin = getPlanarData(x, y, z, z_value)
        extractionObject = DimensionsExtraction(np.vstack((xs, ys)).T, height, pitch)
        temporary = extractionObject.extractDimensions()
        temp2 = extractionObject.checkInversion()
        lowestWidth.append(extractionObject.dimensions[0, 0] + extractionObject.dimensions[0, 1])
        temp3 = getAMatch(temporary, profilePoints)
        #pdb.set_trace()
        """If no match is found, get to the next cross-section"""
        if temp3 == -1:
            if z_value == z_min:
                extrapolateAtStart = True
            # if xForInt.size == 0:
            #     xForInt = xs
            # else:
            #     xForInt = np.append(xForInt, xs, axis=0)
            # if yForInt.size == 0:
            #     yForInt = ys
            # else:
            #     yForInt = np.append(yForInt, ys, axis=0)
            # if zForInt.size == 0:
            #     zForInt = np.full_like(xs, z_value)
            # else:
            #     zForInt = np.append(zForInt, np.full_like(xs, z_value))
            
            if z_value == z_max:
                #pdb.set_trace()
                # if np.max(newData[:, 3]) > np.max(totalData[:, 3]):
                #     pass
                # else:
                try:
                    ends = EndsInterpolation(totalData, None, pitch, height, increments[0] + 1, z_value + 1)
                    newData = ends.interpolation()
                    totalData = np.append(totalData, newData, axis=0)
                except IndexError:
                    pass
                # xForInt = np.array([])
                # yForInt = np.array([])
                # zForInt = np.array([])
            continue
        
        """If it is the first cross-section, directly set the several arrays
        and get the displacement field"""
        if i == 0:
            dimensions[0] = temporary
            inversions[0] = temp2
            increments[0] = z_value
            matches[0] = temp3
            disp1 = getFields(matches[0], inversions[0], youngsModulus)
            disp1[:, 2] = increments[0]
            # maxDis.append(float(np.max(disp1[:, 3])))
            totalData = disp1
            continue

        
        """If it is other than the first cross-section, update the several arrays but
        continue with the current iteration"""
        if i >= 1:
            dimensions[1] = temporary
            inversions[1] = temp2
            increments[1] = z_value
            matches[1] = temp3
        
        """Compare the dimensions of two cross-sections and skip if they are
        almost equivalent"""
        if compareDimensions(dimensions[0], dimensions[1]):
            if totalData.size == 0:
                totalData = getFields(matches[1], inversions[1], youngsModulus)
                totalData[:, 2] = increments[1]
                temporaryNumber = copy.deepcopy(increments[1])
            else:
                disp2 = copy.deepcopy(disp1)
                disp2[:, 2] = increments[1]
                if increments[1] - increments[0] > 1:
                    try:
                        ends = EndsInterpolation(disp1, disp2, pitch, height, increments[0] + 1, increments[1])
                        newData = ends.linearInterpolation()
                        totalData = np.append(totalData, newData, axis=0)
                    except NameError:
                        print("Skipping this interpolation due to the unavailabitity of data")
                increments[0] = copy.deepcopy(increments[1])
                inversions[0] = copy.deepcopy(inversions[1])
                totalData = np.append(totalData, disp2, axis=0)
            continue

        """Obtain the next cross-sectional displacement field"""
        disp2 = getFields(matches[1], inversions[1], youngsModulus)
        disp2[:, 2] = increments[1]

        """Check if the first cross-section didn't find a match"""
        # if totalData.size == 0:
        #     ends = EndsInterpolation(None, disp2, pitch, height, 0, increments[1])
        #     totalData = ends.interpolation()
        #     increments[0] = z_value - 1
            # xForInt = np.array([])
            # yForInt = np.array([])
            # zForInt = np.array([])
        # elif z_value == z_max and temp3 == -1:
        #     ends = EndsInterpolation(disp1, pitch, height, increments[0] + 1, z_max)
        #     newData = ends.interpolation()
        #     totalData = np.append(totalData, newData, axis=0)
        if totalData.size == 0:
            totalData = disp2
            temporaryNumber = copy.deepcopy(increments[1])
        else:
            totalData = np.append(totalData, disp2, axis=0)
        
        """If no matches are found, the difference between two cross-sections
        will be greater than one"""
        if increments[1] - increments[0] > 1:
            try:
                ends = EndsInterpolation(disp1, disp2, pitch, height, increments[0] + 1, increments[1])
                newData = ends.linearInterpolation()
                totalData = np.append(totalData, newData, axis=0)
            except NameError:
                print("Skipping this interpolation due to the unavailabitity of data")
            # totalData = np.append(totalData, disp2, axis=0)
            # xForInt = np.array([])
            # yForInt = np.array([])
            # zForInt = np.array([])
        
        dimensions[0] = dimensions[1]
        increments[0] = increments[1]
        inversions[0] = inversions[1]
        matches[0] = matches[1]
        disp1 = copy.deepcopy(disp2)
        
        # pdb.set_trace()
        
        # if not os.path.exists('../InterpolatedData/' + str(profileName) + '.csv'):
        #     np.savetxt( '../InterpolatedData/' + str(profileName) + '.csv', 
        #                totalData, delimiter=',')
        #     dimensions[0] = dimensions[1]
        #     increments[0] = increments[1]
        #     inversions[0] = inversions[1]
        #     matches[0] = matches[1]
        #     continue
        
        # with open('../InterpolatedData/' + str(profileName) + '.csv', 'ab') as abc:
        #     np.savetxt('../InterpolatedData/' + str(profileName) + '.csv', 
        #                totalData, delimiter=',')
    
    """Check if the first cross-section exterpolation is required"""
    if extrapolateAtStart:
        # pdb.set_trace()
        try:
            ends = EndsInterpolation(None, totalData, pitch, height, 0, temporaryNumber)
        #pdb.set_trace()
            newData = ends.interpolation()
            if np.max(newData[:, 3]) > np.max(totalData[:, 3]):
                pass
            else:
                totalData = np.append(totalData, newData, axis=0)
        except IndexError:
            print("Skipping this interpolation due to unavailability of sufficient data")

    """Delete coordinates whose displacement field is zero"""
    # pdb.set_trace()
    # totalData = np.delete(totalData, np.where(totalData[:, 3] <= 1e-3), axis=0)
    # totalData = np.delete(totalData, np.where(totalData[:, 3] >= 14.), axis=0)

    # """Remove outliers"""
    # pcd = o3d.geometry.PointCloud()
    # pcd.points = o3d.utility.Vector3dVector(totalData[:, 0:3])

    # voxel_down_pcd = pcd.voxel_down_sample(voxel_size=0.02)
    # cl, ind = voxel_down_pcd.remove_radius_outlier(nb_points=10, radius=1)

    # # os.chdir('../InterpolatedData')
    # # os.chdir('../InterpolationTechniques')

    """delX is calculated, i.e the labels"""
    
    # pdb.set_trace()
    for z_value in range(z_min, z_max + 1, 1):
        planarDF = totalData[(totalData[:, 2] == z_value)]
        maxDis.append(np.max(planarDF[:, 3]))

    d = (pitch * 1e-3) - np.array(lowestWidth)
    maxDis = np.asarray(maxDis)
    m = np.max(maxDis)
    dMax = np.max(d[(maxDis == m)])
    if m <= float(dMax * 1e3) / 8:
        collapse.append(0.)
    elif m > np.float(dMax * 1e3) / 8 and m <= float(dMax * 1e3) / 4:
        collapse.append(1.)
    elif m > float(dMax * 1e3) / 4 and m <= float(dMax * 1e3) / 2:
        collapse.append(2.)
    elif m >= float(dMax * 1e3) / 2:
        collapse.append(3.) 
    
    """Save the total data in a single file"""
    np.savetxt( '../InterpolatedData-1/' + str(profileName) + '_' + str(collapse[ii]) + '.csv', totalData, delimiter=',')

    """Point cloud is normalised"""
    # data[:, 0] = data[:, 0] - 0.5 * xLen
    # data[:, 1] = data[:, 1] - 0.5 * zLen
    # data[:, 2] = data[:, 2] - 0.5 * yLen

    # data = data.astype(float)
    # data[:, 0] = np.true_divide(2 * (data[:, 0] + 0.5 * xLen), xLen) - 1
    # data[:, 1] = np.true_divide(2 * (data[:, 1] + 0.5 * zLen), zLen) - 1
    # data[:, 2] = np.true_divide(2 * (data[:, 2] + 0.5 * yLen), yLen) - 1

    # np.save('../NormalisedProfiles/' + str(profileName) + '.npy', data)
    data_all[ii] = str(profile)

f.create_dataset("clouds", data=data_all, compression="gzip")
f.create_dataset("labels", data=np.asarray(collapse).astype(int))
f.close()