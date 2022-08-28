# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 10:15:07 2021

@author: arava
"""

import numpy as np
import pdb

class Stencil:
    def __init__(self, pointFromGrid, dataSet, tolerance):
        self.pointFromGrid = pointFromGrid
        self.dataSet = dataSet
        self.tolerance = tolerance
        self.extractedPoints = np.array([])
        self.iterator = 0
    
    def extractPoints(self):
        for dataPoint in self.dataSet:
            # Initial extraction in xy plane
            dataPoint = np.array(dataPoint, dtype=float)
            
            fromFields = np.isclose(dataPoint[0:2], self.pointFromGrid[0:2], rtol=self.tolerance)
            
            # Add the corresponding point if either of the conditions are satisified
            if np.all(fromFields):
                # pdb.set_trace()
                self.extractedPoints = np.append(self.extractedPoints, dataPoint, axis=0)
                self.iterator += 1
                continue
            
            # # Check for data points that are already evaluated and found
            # x_y = np.equal(dataPoint[1:3], self.pointFromGrid[0:2])
            # y_z = np.equal(dataPoint[2:4], self.pointFromGrid[1:3])
            # x_z = np.equal(dataPoint[[1, 3]], self.pointFromGrid[[0, 2]])
            
            # if np.all(x_y) or np.all(y_z) or np.all(x_z):
            #     self.extractedPoints = np.append(self.extractedPoints, dataPoint, axis=0)
            #     self.iterator += 1
            
        self.extractedPoints = self.extractedPoints.reshape((self.iterator, 4))
        # print('The number of points extracted are ' + str(self.iterator))
            
        return self.extractedPoints
