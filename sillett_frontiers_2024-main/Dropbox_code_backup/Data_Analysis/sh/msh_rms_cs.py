## Script to calculate rms error

import argparse
import pyvista as pv
import numpy as np
from sklearn.metrics import mean_squared_error

parser = argparse.ArgumentParser(description='Compare 2 meshes for verification test')

parser.add_argument('--msh1', required=True, help='mesh 1')
parser.add_argument('--msh2', required=True, help='mesh 2')
parser.add_argument('--save-txt', action='store_true')

args = parser.parse_args()

# Read meshes
msh1 = pv.read(args.msh1)
msh2 = pv.read(args.msh2)

# Get point coords
msh1_pts = np.array(msh1.points)
msh2_pts = np.array(msh2.points)

# print("msh1_pts shape: ", msh1_pts.shape)
# print("msh2_pts shape: ", msh2_pts.shape)

# initialise array
rmse_t = np.zeros((9,))

rmse = mean_squared_error(msh1_pts, msh2_pts, squared=False)

print(rmse)