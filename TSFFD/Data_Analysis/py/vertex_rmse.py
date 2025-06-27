"""
Use this script to plot and save rms transient data as part of FT verification.
"""

import argparse
import pyvista as pv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

parser = argparse.ArgumentParser(description='Compare 2 meshes for verification test')

parser.add_argument('--motionPath', required=True, help='original tracking path')
parser.add_argument('--veriMotionPath', required=True, help='verification tracking path')
parser.add_argument('--save-txt', action='store_true')
parser.add_argument('--save-png', action='store_true')
parser.add_argument('--numTimes', help='number of frames [10]', default=10)

args = parser.parse_args()

# initialise array
rmse_t = np.zeros((9,))

for frame in range(1,10):
	# Read meshes
	msh1 = pv.read(f'{args.motionPath}/transformed-{frame}-clip.vtu')
	msh2 = pv.read(f'{args.veriMotionPath}/transformed-{frame}-clip.vtu')

	# Get point coords
	msh1_pts = np.array(msh1.points)
	msh2_pts = np.array(msh2.points)

	# print("msh1_pts shape: ", msh1_pts.shape)
	# print("msh2_pts shape: ", msh2_pts.shape)

	rmse = mean_squared_error(msh1_pts, msh2_pts, squared=False)

	rmse_t[frame-1] = rmse
	print(rmse)

if args.save_txt:
	print("Saving txt")
	np.savetxt(f'{args.veriMotionPath}/rms_verification.txt', rmse_t)

## Plot

# PLot
fig, (ax1) = plt.subplots(1,1,figsize=(7,5))

normTime=np.arange(1, args.numTimes)/args.numTimes

ax1.plot(normTime, rmse_t)

ax1.set(xlabel='Time (normalised)')
ax1.set(ylabel='msh vertex rmse')
ax1.label_outer()
ax1.grid(True)

if args.save_png:
	print("Saving png")
	fig.savefig(f'{args.veriMotionPath}/rmse_transient.png', dpi=200)

# plt.show()