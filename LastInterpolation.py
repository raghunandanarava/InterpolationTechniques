from textwrap import fill
import numpy as np
from scipy.interpolate import griddata
from scipy.interpolate import Rbf
import pdb

class Interpolation:
    def __init__(self, data, zS, pitch, height):
        """Input arguments are set"""
        self.data = data
        self.zS = zS

        self.x_ = np.linspace(np.min(self.data[:, 0]), np.max(self.data[:, 0]), num=int(pitch))
        self.y_ = np.linspace(np.min(self.data[:, 1]), np.max(self.data[:, 1]), num=int(height))

        self.xMesh, self.yMesh, self.zMesh = np.meshgrid(self.x_, self.y_, self.zS, indexing='ij')

        self.produceStructuredData()

    
    def produceStructuredData(self):
        xMesh, yMesh, zMesh = np.meshgrid(self.x_, self.y_, np.unique(self.data[:, 2]), indexing='ij')
        structuredValues = griddata(self.data[:, 0:3], self.data[:, 3], (xMesh, yMesh, zMesh), method='linear', fill_value=0)
        self.data = np.stack((xMesh.flatten(), yMesh.flatten(), zMesh.flatten(), structuredValues.flatten()), axis=-1)

    def Interpolate(self):
        interValue = Rbf(self.data[:, 0], self.data[:, 1], self.data[:, 2], self.data[:, 3], smooth=3)
        interValue = interValue(self.xMesh, self.yMesh, self.zMesh)
        interValue = np.stack((self.xMesh.flatten(), self.yMesh.flatten(), self.zMesh.flatten(), interValue.flatten()), axis=-1)
        self.data = np.append(self.data, interValue, axis=0)
        return self.data