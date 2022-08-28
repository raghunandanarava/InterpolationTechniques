# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 12:01:02 2021

@author: arava
"""
import numpy as np
    

class Linear:
    def __init__(self, points):
        self.points = points
    
    def Interpolate(self):
        Matrix = np.zeros((self.points.shape[0], 8), dtype=float)
        Matrix[:, 0] = 1
        Matrix[:, 1] = self.points[:, 0]
        Matrix[:, 2] = self.points[:, 1]
        Matrix[:, 3] = self.points[:, 2]
        Matrix[:, 4] = np.multiply(self.points[:, 0], self.points[:, 1])
        Matrix[:, 5] = np.multiply(self.points[:, 0], self.points[:, 2])
        Matrix[:, 6] = np.multiply(self.points[:, 1], self.points[:, 2])
        Matrix[:, 7] = np.multiply(self.points[:, 0], np.multiply(self.points[:, 1], self.points[:, 2]))
        
        self.coefficients = np.matmul(np.linalg.pinv(Matrix), self.points[:, 3])
        
    def function(self, gridPoint):
        return (self.coefficients[0] + (self.coefficients[1] * gridPoint[0]) + 
                (self.coefficients[2] * gridPoint[1]) + (self.coefficients[3] * gridPoint[2])
                + (self.coefficients[4] * gridPoint[0] * gridPoint[1]) + (self.coefficients[5] * gridPoint[0] * gridPoint[2])
                + (self.coefficients[6] * gridPoint[1] * gridPoint[2]) + (self.coefficients[7] * gridPoint[0] * gridPoint[1] * gridPoint[2]))

class Cubic:
    def __init__(self, points):
        self.x = points[:, 0]
        self.y = points[:, 1]
        self.z = points[:, 2]
        self.value = points[:, 3]
    
    def Interpolate(self):
        tmpNumber = 0
        Matrix = np.zeros((self.x.shape[0], 64), dtype=float)
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    Matrix[:, tmpNumber] = (self.x ** i) * (self.y ** j) * (self.z ** k)
                    tmpNumber += 1
        
        self.coefficients = np.matmul(np.linalg.pinv(Matrix), self.value)
    
    def function(self, gridPoint):
        functionValue = 0
        tmpNumber = 0
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    functionValue += self.coefficients[tmpNumber] * (gridPoint[0] ** i) * (gridPoint[1] ** j) * (gridPoint[2] ** k)
                    tmpNumber += 1
        return functionValue