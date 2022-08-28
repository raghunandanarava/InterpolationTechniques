# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 15:17:35 2021

@author: arava
"""


"""Required modules are imported here"""
import numpy as np
# from InitialComparison import *
# from RefactorDesignPoints import *
from Compare import *
# from GetDesignPointsFile import *
from Data_Conglomeration import *
import os

"""Extraction of points at a particular cross-section"""
def getPlanarData(x, y, z, zMin):
    new_x = x[(z == zMin)]
    new_y = y[(z == zMin)]
    min_y = np.min(new_y)
    max_y = np.max(new_y)
    return new_x, new_y, min_y

"""Compare two cross-sections data"""
def compareDimensions(dimension_1, dimension_2):
    result = np.isclose(dimension_1, dimension_2, atol=0.001)
    return np.all(result)

"""Compare the cross-sectional dimensions with the data points"""
def getAMatch(dimension, refactor):
    compareDimensionsObject = CompareDimensions(dimension, refactor)
    match = compareDimensionsObject.compareToGetAMatch()
    return match

"""Interpolation Between Two Fields"""
def interpolationTechnique(displace1, displace2, pitch, height):
    
    dispObj = DataConglomeration(displace1, displace2, pitch, height)
    newData = dispObj.carryOut()
    return newData
    
# """Comparison and Interpolation"""
# def compareAndInterpolate(xs, ys, zs, z_value, iterator, dimensions,
#                           i, profileName, pitch, height):
#     """Extract points in a particular cross-section"""
#     xNew, yNew, yMin = getPlanarData(xs, ys, zs, z_value)
    
#     """Extract dimensions at the cross-section"""
#     dimensionObject = Compare(np.vstack((xNew, yNew)).T, height)
#     extractedDimensions = dimensionObject.extractDimensions()
    
#     """Check if the z_value is the the least, i.e the first cross-section of
#     the rough profile"""
#     if dimensions.shape == 0:
#         return extractedDimensions
    
#     """check if the dimensions are similar"""
#     check = compareDimensions(dimensions, extractedDimensions)
    
#     if check:
#         dimensions = compareAndInterpolate(xs, ys, zs, z_value + 1, iterator, 
#                                            dimensions, i, profileName, pitch, 
#                                            height)
#         return dimensions