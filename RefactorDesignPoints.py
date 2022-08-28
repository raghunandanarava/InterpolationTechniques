# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 11:33:47 2021

@author: arava
"""

import numpy as np

class Refactorisation:
    def __init__(self, designPoints):
        self.designPoints = designPoints
        self.refactored = np.zeros((np.shape(designPoints)[0], 17))
    
    def refactor(self):
        self.refactored[:, 0] = self.designPoints[:, 0]
        self.refactored[:, 1] = self.designPoints[:, 2]
        self.refactored[:, 2] = self.designPoints[:, 3]
        self.refactored[:, 3] = self.designPoints[:, 4]
        self.refactored[:, 4] = self.designPoints[:, 5]
        self.refactored[:, 5] = self.designPoints[:, 7]
        self.refactored[:, 6] = self.designPoints[:, 8]
        self.refactored[:, 7] = self.designPoints[:, 10]
        self.refactored[:, 8] = self.designPoints[:, 11]
        self.refactored[:, 9] = self.designPoints[:, 13]
        self.refactored[:, 10] = self.designPoints[:, 14]
        self.refactored[:, 11] = self.designPoints[:, 6]
        self.refactored[:, 12] = self.designPoints[:, 9]
        self.refactored[:, 13] = self.designPoints[:, 12]
        self.refactored[:, 14] = self.designPoints[:, 15]
        self.refactored[:, 15] = self.designPoints[:, 1]
        self.refactored[:, 16] = self.designPoints[:, 16]

        # self.refactored[:, 0] = self.designPoints[:, 0]
        # self.refactored[:, 1] = self.designPoints[:, 2]
        # self.refactored[:, 2] = self.designPoints[:, 3]
        # self.refactored[:, 3] = self.designPoints[:, 4] + self.designPoints[:, 5]
        # self.refactored[:, 4] = self.designPoints[:, 7] + self.designPoints[:, 8]
        # self.refactored[:, 5] = self.designPoints[:, 10] + self.designPoints[:, 11]
        # self.refactored[:, 6] = self.designPoints[:, 13]
        # self.refactored[:, 7] = self.designPoints[:, 14]
        # self.refactored[:, 8] = self.designPoints[:, 6]
        # self.refactored[:, 9] = self.designPoints[:, 9]
        # self.refactored[:, 10] = self.designPoints[:, 12]
        # self.refactored[:, 11] = self.designPoints[:, 15]
        # self.refactored[:, 12] = self.designPoints[:, 1]
        # self.refactored[:, 13] = self.designPoints[:, 16]

        # self.refactored[:, 0] = self.designPoints[:, 0]
        # self.refactored[:, 1] = self.designPoints[:, 2] + self.designPoints[:, 3]
        # self.refactored[:, 2] = self.designPoints[:, 4] + self.designPoints[:, 5]
        # self.refactored[:, 3] = self.designPoints[:, 7] + self.designPoints[:, 8]
        # self.refactored[:, 4] = self.designPoints[:, 10] + self.designPoints[:, 11]
        # self.refactored[:, 5] = self.designPoints[:, 13] + self.designPoints[:, 14]
        # self.refactored[:, 6] = self.designPoints[:, 6]
        # self.refactored[:, 7] = self.designPoints[:, 9]
        # self.refactored[:, 8] = self.designPoints[:, 12]
        # self.refactored[:, 9] = self.designPoints[:, 15]
        # self.refactored[:, 10] = self.designPoints[:, 1]
        
        return self.refactored