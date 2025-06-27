##  Plot and save rms transient from verification step

import pandas as pd
import argparse
import pyvista as pv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

parser = argparse.ArgumentParser(description="Compare 2 meshes' strains for verification test")

parser.add_argument('--motionPath', required=True, help='original tracking path')
parser.add_argument('--veriMotionPath', required=True, help='verification tracking path')
parser.add_argument('--strainType', required=True, help='either area or fibre_arch')
parser.add_argument('--save-txt', action='store_true')
parser.add_argument('--save-png', action='store_true')
parser.add_argument('--numTimes', help='number of frames [10]', default=10)
parser.add_argument('--UAC', required=True, help="uac with region labels (LCoords_2D_R_v3_C-regional_labels.vtk)")

args = parser.parse_args()

# initialise array
rmse_t = np.zeros((9,))

## For strain RMSE comparison 
## 
## Ensure to only use LA label cells to compare strains
## Aside: Use only 99.5 percentile?

## Read in 2D UAC and extract region labels
uac_msh = pv.read(f"{args.UAC}")
region_label_ar = np.array(uac_msh.cell_data['region_label_v2'])

if args.strainType=="area":
	print("Area strain RMSE:")

	for frame in range(1,10):
		sim_strain = pd.read_csv(f"{args.veriMotionPath}/area-strains-{frame}.csv", skiprows=1, names=["ind", "Area"])
		gt_strain = pd.read_csv(f"{args.motionPath}/area-strains-{frame}.csv", skiprows=1, names=["ind", "Area"])

		# print("gt_strain shape: ", gt_strain.shape)
		# print("region_label_ar num True: ", np.sum([region_label_ar!=0.0]))

		## Include only LA body label
		sim_strain = sim_strain[region_label_ar!=0.0]
		gt_strain = gt_strain[region_label_ar!=0.0]

		# print("gt_strain shape: ", gt_strain.shape)

		# Get difference between strains
		rmse = mean_squared_error(gt_strain['Area'], sim_strain['Area'], squared=False)

		rmse_t[frame-1] = rmse
		print(rmse)

elif args.strainType in ["endo_avg", "epi_avg"]:
	print("Fiber strain RMSE:")

	for frame in range(1,10):
		sim_strain = pd.read_csv(f"{args.veriMotionPath}/{args.strainType}-strains-t{frame}.txt", names=['f1', 'f2', 'f3'], sep=' ', skiprows=2)
		gt_strain = pd.read_csv(f"{args.motionPath}/{args.strainType}-strains-t{frame}.txt", names=['f1', 'f2', 'f3'], sep=' ', skiprows=2)

		# print("gt_strain shape: ", gt_strain.shape)
		# print("region_label_ar num True: ", np.sum([region_label_ar!=0.0]))

		## Include only LA body label
		sim_strain = sim_strain[region_label_ar!=0.0]
		gt_strain = gt_strain[region_label_ar!=0.0]

		# print("gt_strain shape: ", gt_strain.shape)

		# Get difference between strains
		rmse = mean_squared_error(gt_strain['f1'], sim_strain['f1'], squared=False)

		rmse_t[frame-1] = rmse
		print(rmse)

if args.save_txt:
	print("Saving txt")
	np.savetxt(f'{args.veriMotionPath}/{args.strainType}_strain_rmse.txt', rmse_t)

## Plot

# PLot
fig, (ax1) = plt.subplots(1,1,figsize=(7,5))

normTime=np.arange(1, args.numTimes)/args.numTimes

ax1.plot(normTime, rmse_t*100)

ax1.set(xlabel='Time (normalised)')

if args.strainType in ["endo_avg", "epi_avg"]:
	ax1.set(ylabel=f'{args.strainType} f1 strain RMSE [%]')
	save_name = f"{args.strainType}_f1_strain_rmse_transient.png"

elif args.strainType=="area":
	ax1.set(ylabel=f'{args.strainType} strain RMSE [%]')
	save_name = f"{args.strainType}_strain_rmse_transient.png"

ax1.label_outer()
ax1.grid(True)

if args.save_png:
	print("Saving png")
	fig.savefig(f'{args.veriMotionPath}/{save_name}.png', dpi=200)

# plt.show()