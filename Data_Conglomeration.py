# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 15:18:14 2021

@author: arava
"""

import numpy as np
from Stencils import *
from Interpolation import *
from scipy.interpolate import griddata
import pdb

class DataConglomeration:
    def __init__(self, disp1, disp2, pitch, height):
        """Set the displacement field"""
        self.disp = np.append(disp1, disp2, axis=0)
        
        """Extract minimum and maximum coordinates of x and y"""
        xMin = np.min(self.disp[:, 0])
        xMax = np.max(self.disp[:, 0])
        yMin = np.min(self.disp[:, 1])
        yMax = np.max(self.disp[:, 1])
        
        """Define the mesh"""
        self.xMesh, self.yMesh = np.mgrid[xMin: xMax: (pitch * 1j), 
                                          yMin: yMax: (height * 1j)]
        # pdb.set_trace()
        
        """Convert to structured grids"""
        temp1 = griddata(disp1[:, 0:2], np.expand_dims(disp1[:, 3], axis=1), 
                         (self.xMesh, self.yMesh), method='linear', fill_value=0)
        temp2 = griddata(disp2[:, 0:2], np.expand_dims(disp2[:, 3], axis=1), 
                         (self.xMesh, self.yMesh), method='linear', fill_value=0)
        
        
        """Post-Processing"""
        self.xMesh = self.xMesh.flatten()
        self.yMesh = self.yMesh.flatten()
        temp1 = temp1.flatten()
        temp2 = temp2.flatten()
        
        self.zValues = np.arange(np.min(self.disp[:, 2] + 1), 
                                 np.max(self.disp[:, 2]), 1)
        
        temp1 = np.stack((self.xMesh, 
                          self.yMesh, 
                          np.full(self.xMesh.shape, np.min(self.disp[:, 2])),
                          temp1), axis=0).T
        temp2 = np.stack((self.xMesh, 
                          self.yMesh, 
                          np.full(self.xMesh.shape, np.max(self.disp[:, 2])),
                          temp2), axis=0).T
        
        self.disp = np.append(temp1, temp2, axis=0)
        self.disp = np.delete(self.disp, (self.disp[:, 3] == 0.), axis=0)
        
        self.xMesh = np.unique(self.xMesh)
        self.yMesh = np.unique(self.yMesh)
        
        self.newData = np.array([])
        self.toleranceValue = 0.045
    
    
    """Class function which performs the interpolation technique"""
    def carryOut(self):
        """Looping over z, x, and y"""
        for z in self.zValues:
            for x in self.xMesh:
                for y in self.yMesh:
                    gridPoint = np.array([x, y, z]).T
                    
                    """Stencil object creation and in-line points extraction"""
                    stencilObj = Stencil(gridPoint, self.disp, 
                                         self.toleranceValue)
                    extractedPoints = stencilObj.extractPoints()
                    
                    # pdb.set_trace()
                    """Interpolation at the grid point"""
                    # interObj = Cubic(extractedPoints)
                    # interObj.Interpolate()
                    # interValue = interObj.function(gridPoint)
                    
                    interValue = griddata(extractedPoints[:, 2], 
                                          extractedPoints[:, 3], z, 
                                          method='linear', fill_value=0)
                    
                    """Adding the interpolated value into the data"""
                    if self.newData.size == 0:
                        self.newData = np.array([x, y, z, interValue])
                    else:
                        self.newData = np.vstack((self.newData, 
                                                  np.array([x, y, z, interValue])))

        return self.newData