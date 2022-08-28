# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:12:01 2021

@author: raghu
"""
import numpy as np
import pdb

from numpy.core.fromnumeric import size

class CompareDimensions:
    def __init__(self, dimension, designPoints):
        self.dimension = np.squeeze(dimension.T, axis=1)
        self.designPoints = designPoints
        self.match = -1
        self.widthResult = np.empty((self.designPoints.shape[0], 10))

    def compareToGetAMatch(self):
        """Obtain the comparisons with a tolerance"""
        for i, designPoint in enumerate(self.designPoints):
            self.widthResult[i] = np.isclose(designPoint[1:11], self.dimension[0:10], atol=0.002)
        
        """Check where all comparisons have returned true"""
        # check = np.all(self.widthResult, axis=0)
        # matchMask = (self.designPoints[1:6] == self.dimension[0:5]).all(axis=1)
        # Iterate over the design points
        # for i, designPoint in enumerate(self.designPoints):
        #     # Comparing the dimensions extracted with the design points
        #     self.widthResult[i, 0:2] = np.isclose(designPoint[1:3], self.dimension[0:2], rtol=0, atol=0.001)
        #     self.widthResult[i, 2:5] = np.isclose(designPoint[3:6], self.dimension[2:5], rtol=0, atol=0.001)
        #     self.widthResult[i, 5:7] = np.isclose(designPoint[6:8], self.dimension[5:7], rtol=0, atol=0.001)
            # heightResult = np.isclose(designPoint[6:10], self.dimension[5:9])
            
            # A check to see if a match was found and breaking from the loop if found  np.all(heightResult)
            # if np.all(widthResult):
            #     self.match = int(ndesignPoint[0])
            #     print(self.match)
            #     break
        # probabilities = self.widthResult.sum(axis=1)
        """Extract the design points whose top three widths are approximately equal"""
        probabilities = self.widthResult[:, :4].sum(axis=1)
        newPoints = self.designPoints[(probabilities >= 3)]
        newWidthResult = self.widthResult[(probabilities >= 3)]

        probabilities = newWidthResult[:, 4:].sum(axis=1)
        newPoints = newPoints[(probabilities >= 5)]
        newWidthResult = newWidthResult[(probabilities >= 5)]

        #pdb.set_trace()
        if newPoints.size == 0:
            return self.match
        if newPoints.size == 1:
            self.match = int(newPoints[0, 0])
        else:
            self.match = int(np.random.choice(newPoints[:, 0], size=1, replace=False))
        return self.match
