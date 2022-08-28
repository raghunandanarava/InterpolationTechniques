# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 10:49:03 2021

@author: arava
"""
import numpy as np
import random
import pdb

class DimensionsExtraction:
    def __init__(self, resistProfile, profileHeight, pitch):
        self.x = resistProfile[:, 0]
        self.y = resistProfile[:, 1]
        self.profileHeight = profileHeight
        self.pitch = pitch
        self.dimensions = np.zeros((1, 14))
        # self.dimensions = np.zeros((1, 11))
        self.dimensions[0, 10] = self.dimensions[0, 11] = self.dimensions[0, 12] = self.dimensions[0, 13] = (self.profileHeight / 4) * 1e-3
        # self.dimensions[0, 7] = self.dimensions[0, 8] = self.dimensions[0, 9] = self.dimensions[0, 10] = (self.profileHeight / 4) * 1e-3
        self.match = None
    
    def extractDimensions(self):
        
        """Extract the bottom height coordinate and the
        bottom width coordinates"""
        # pdb.set_trace()
        yMin = np.min(self.y)
        x_values = self.x[(self.y == round(yMin))]

        """Extract the minimum and maximum coordinates of the width at the lowest height"""
        xMin = np.min(self.x[(self.y == round(yMin))])
        xMax = np.max(self.x[(self.y == round(yMin))])

        """Set the lowers two widths"""
        self.dimensions[0, 0] = (self.pitch - xMin) * 1e-3
        self.dimensions[0, 1] = (xMax - self.pitch) * 1e-3

        """Looping over to set the remainder widths"""
        for i in range(2, 10, 2):

            """Incremented Height"""
            yMin += (self.profileHeight / 4)

            """Extract the minimum and maximum coordinates of the width at that height"""
            xMin = np.min(self.x[(self.y == round(yMin))])
            xMax = np.max(self.x[(self.y == round(yMin))])

            """Calculate widths"""
            self.dimensions[0, i] = (self.pitch - xMin) * 1e-3
            self.dimensions[0, i + 1] = (xMax - self.pitch) * 1e-3
        
        # """Extract maximum height coordinate"""
        # yMax = np.max(self.y)
        # x_values = self.x[(self.y == yMax)]
        # xMin = np.min(self.x[(self.y == round(yMax))])
        # xMax = np.max(self.x[(self.y == round(yMax))])
        
        # """Set the upper two widths"""
        # self.dimensions[0, 5] = (x_mid - xMin) * 1e-3
        # self.dimensions[0, 6] = (xMax - x_mid) * 1e-3

        return np.array(self.dimensions)

        # for i in range(0, 10, 2):

        #     """Extract the minimum and maximum coordinates of the width at that height"""
        #     xMin = np.min(self.x[(self.y == round(yMin))])
        #     xMax = np.max(self.x[(self.y == round(yMin))])

        #     """Widths are calculated"""
        #     self.dimensions[:, i] = (x_mid - xMin) * 1e-3
        #     self.dimensions[:, i + 1] = (xMax - x_mid) * 1e-3

        #     """Height is incremented"""
        #     yMin += (self.profileHeight / 4)
        
        # """Returning the dimensions of the cross-section as an array"""
        # return np.array(self.dimensions)

        #Extract the bottom coordinate of the height
        # yMin = np.min(self.y)
        # x_values = self.x[(self.y == round(yMin))]
        
        # for i in range(0, 5, 1):
            
        #     # pdb.set_trace()
        #     # Minimum and Maximum coordinates of the width at that height
        #     xMin = np.min(self.x[(self.y == round(yMin))])
        #     xMax = np.max(self.x[(self.y == round(yMin))])
            
        #     # Widths are calculated
        #     self.dimensions[:, i] = (xMax - xMin) * 1e-3
            
        #     yMin = yMin + (self.profileHeight / 4)
        
        # return np.array(self.dimensions)
    
    def checkInversion(self):
        # A check for inversion by comparing the bottom width with the top width
        if self.dimensions[0, 0] + self.dimensions[0, 1] > self.dimensions[0, 8] + self.dimensions[0, 9]:
            return True
        else:
            return False
        # if dim[0] > dim[4]:
        #     return True
        # else:
        #     return False