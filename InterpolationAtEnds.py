import numpy as np
from numpy.lib.function_base import extract
from scipy.interpolate import griddata
from scipy.interpolate import Rbf
from Stencils import *

class EndsInterpolation:
    def __init__(self, disp1, disp2, pitch, height, increment1, increment2):
        "Set the displacement field and increment value"
        self.disp1 = disp1
        self.disp2 = disp2
        self.increment1 = int(increment1)
        self.increment2 = int(increment2)

        # self.x = x
        # self.y = y
        # self.z = z

        """Extract minimum and maximum coordinates of x and y"""
        

        """Define the mesh"""

        
        """Convert to structured grids"""
        if self.disp1 is None:
            #pdb.set_trace()
            xMin = np.min(self.disp2[:, 0])
            xMax = np.max(self.disp2[:, 0])
            yMin = np.min(self.disp2[:, 1])
            yMax = np.max(self.disp2[:, 1])

            self.xMesh, self.yMesh = np.mgrid[xMin : xMax : (pitch * 1j), yMin : yMax : (height * 1j)]
            self.disp = griddata(self.disp2[:, 0:2], np.expand_dims(self.disp2[:, 3], axis=1), (self.xMesh, self.yMesh), method='linear', fill_value=0)
            self.disp = np.stack((self.xMesh.flatten(), self.yMesh.flatten(), np.full_like(self.xMesh, self.increment2).flatten(), self.disp.flatten()), axis=0).T
            self.smooth = 5
        elif self.disp2 is None:
            xMin = np.min(self.disp1[:, 0])
            xMax = np.max(self.disp1[:, 0])
            yMin = np.min(self.disp1[:, 1])
            yMax = np.max(self.disp1[:, 1])

            self.xMesh, self.yMesh = np.mgrid[xMin : xMax : (pitch * 1j), yMin : yMax : (height * 1j)]
            self.disp = griddata(self.disp1[:, 0:2], np.expand_dims(self.disp1[:, 3], axis=1), (self.xMesh, self.yMesh), method='linear', fill_value=0)
            self.disp = np.stack((self.xMesh.flatten(), self.yMesh.flatten(), np.full_like(self.xMesh, self.increment1).flatten(), self.disp.flatten()), axis=0).T
            self.smooth = 5
        else:
            xMin = np.min(np.append(self.disp1[:, 0], self.disp2[:, 0], axis=0))
            xMax = np.max(np.append(self.disp1[:, 0], self.disp2[:, 0], axis=0))
            yMin = np.min(np.append(self.disp1[:, 1], self.disp2[:, 1], axis=0))
            yMax = np.max(np.append(self.disp1[:, 1], self.disp2[:, 1], axis=0))

            self.xMesh, self.yMesh = np.mgrid[xMin : xMax : (pitch * 1j), yMin : yMax : (height * 1j)]
            self.disp1 = griddata(self.disp1[:, 0:2], np.expand_dims(self.disp1[:, 3], axis=1), (self.xMesh, self.yMesh), method='linear', fill_value=0)
            self.disp1 = np.stack((self.xMesh.flatten(), self.yMesh.flatten(), np.full_like(self.xMesh, self.increment1).flatten(), self.disp1.flatten()), axis=0).T
            self.disp2 = griddata(self.disp2[:, 0:2], np.expand_dims(self.disp2[:, 3], axis=1), (self.xMesh, self.yMesh), method='linear', fill_value=0)
            self.disp2 = np.stack((self.xMesh.flatten(), self.yMesh.flatten(), np.full_like(self.xMesh, self.increment2).flatten(), self.disp2.flatten()), axis=0).T

            self.disp = np.append(self.disp1, self.disp2, axis=0)

            self.smooth = 0
        
        # """Post processing"""
        # self.xMesh = self.xMesh.flatten()
        # self.yMesh = self.yMesh.flatten()
        # self.disp = self.disp.flatten()

        # self.disp = np.stack((self.xMesh, self.yMesh, np.full(self.xMesh.shape, np.min(disp[:, 2])), self.disp), axis=0).T
        # self.disp = np.delete(self.disp, (self.disp[:, 3] == 0.), axis=0)

        # self.xMesh = np.unique(self.xMesh)
        # self.yMesh = np.unique(self.yMesh)

        self.newData = np.array([])
        # self.tolerance = max((xMax - xMin) / pitch, (yMax - yMin) / height)
    
    """Class function which performs the interpolation technique"""
    def interpolation(self):
        """Looping over x, y, and z"""
        for z in range(self.increment1, self.increment2):
            interValue = Rbf(self.disp[:, 0], self.disp[:, 1], self.disp[:, 2], self.disp[:, 3], function='gaussian', smooth=self.smooth)
            interValue = interValue(self.xMesh, self.yMesh, np.full_like(self.xMesh, z))

            if self.newData.size == 0:
                self.newData = np.array([self.xMesh.flatten(), self.yMesh.flatten(), np.full_like(self.xMesh, z).flatten(), interValue.flatten()]).T
            else:
                self.newData = np.append(self.newData, np.array([self.xMesh.flatten(), self.yMesh.flatten(), np.full_like(self.xMesh, z).flatten(), interValue.flatten()]).T, axis=0)
            

            
        #     for y in self.yMesh:
        #         for x in self.xMesh:
        #             gridPoint = np.array([x, y, z]).T

        #             """Stencil object creation and in-line points extraction"""
        #             stencilObj = Stencil(gridPoint, self.disp, tolerance=self.tolerance)
        #             extractedPoints = stencilObj.extractPoints()

        #             """Extrapolation at the grid point"""
        #             interValue = Rbf(extractedPoints[:, 0], extractedPoints[:, 1], extractedPoints[:, 2], extractedPoints[:, 3], smooth=5)
        #             interValue = interValue(x, y, z)
        #             # interValue = griddata(extractedPoints[:, 2], 
        #             #                       extractedPoints[:, 3], z, 
        #             #                       method='linear', fill_value=0)
                    
        #             """Adding the interpolated value into the data"""
        #             if self.newData.size == 0:
        #                 self.newData = np.array([x, y, z, interValue])
        #             else:
        #                 self.newData = np.vstack((self.newData, 
        #                                           np.array([x, y, z, interValue])))
        return self.newData
    
    def linearInterpolation(self):
        for z in range(self.increment1, self.increment2):
            interValue = griddata((self.disp[:, 0], self.disp[:, 1], self.disp[:, 2]), self.disp[:, 3], (self.xMesh, self.yMesh, np.full_like(self.xMesh, z)), method='linear', fill_value=0)
            if self.newData.size == 0:
                self.newData = np.array([self.xMesh.flatten(), self.yMesh.flatten(), np.full_like(self.xMesh, z).flatten(), interValue.flatten()]).T
            else:
                self.newData = np.append(self.newData, np.array([self.xMesh.flatten(), self.yMesh.flatten(), np.full_like(self.xMesh, z).flatten(), interValue.flatten()]).T, axis=0)
            
        return self.newData