import numpy as np
from scipy.interpolate.fitpack2 import InterpolatedUnivariateSpline
from InterpolationAtEnds import *
from GetDesignPointsFile import *

def Interpolation(disp1, disp2, pitch, height, increment1, increment2):
    ends = EndsInterpolation(disp1, disp2, pitch, height, increment1, increment2)
    newData = ends.linearInterpolation()
    return newData

design_numbers = ['0', '6', '16', '20', '28', '34']
x_offset = [0, 0.002, -0.002, 0.002, -0.002, -0.002]
# z_offset = [0, 100, 200, 300, 400, 500]
temp = 0
data = np.asarray([])

for i in range(5):
    disp1 = getFields(design_numbers[i], False, 0.3)
    disp2 = getFields(design_numbers[i + 1], False, 0.3)

    disp1[:, 1] = disp1[:, 1] + x_offset[i]
    disp2[:, 1] = disp2[:, 1] + x_offset[i + 1]

    # disp1[:, 2] = z_offset[i]
    # disp2[:, 2] = z_offset[i + 1]

    new = np.append(disp1, disp2, axis=0)
    
    newData = Interpolation(disp1, disp2, 28, 35, temp, temp + 100)
    if data.size == 0:
        data = new
    else:
        data = np.append(data, new, axis=0)

    data = np.append(data, newData, axis=0)
    temp = temp + 100

np.savetxt('../InterpolatedData-1/InterpolationTestResult.csv', data, delimiter=',')