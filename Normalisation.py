import numpy as np
import os

"""Rough Profiles' names are obtained"""
roughProfiles = os.listdir('../../RoughProfilesGeneration/Resist-Profiles/')

for profile in roughProfiles:
    profileName = str(profile).split('.npy')[0]
    nothing = str(profile).split('_')

    xLen = float(nothing[15])
    zLen = float(nothing[16])
    yLen = float(nothing[17].split('.')[0])

    data = np.load('../../RoughProfilesGeneration/Resist-Profiles/' + str(profile))

    """Point cloud is normalised"""
    data[:, 0] = data[:, 0] - 0.5 * xLen
    data[:, 1] = data[:, 1] - 0.5 * zLen
    data[:, 2] = data[:, 2] - 0.5 * yLen

    data = data.astype(float)
    data[:, 0] = np.true_divide(2 * (data[:, 0] + 0.5 * xLen), xLen) - 1
    data[:, 1] = np.true_divide(2 * (data[:, 1] + 0.5 * zLen), zLen) - 1
    data[:, 2] = np.true_divide(2 * (data[:, 2] + 0.5 * yLen), yLen) - 1

    np.save('../NormalisedProfiles/' + str(profileName) + '.npy', data)