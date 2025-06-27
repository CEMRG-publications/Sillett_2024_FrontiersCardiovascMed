## Plots global mean fibre strain transients

## Update 21st April 2023
## Following AWCL Chat: use scaled jacobian as msh quality check before calculating strains

import matplotlib.pyplot as plt
import pandas as pd
import argparse
import numpy as np
import pyvista as pv

DataPath="/home/csi20/Dropbox/phd/Data/RG_CT_Cases"
DataPath="/home/csi20local/Dropbox/phd/Data/RG_CT_Cases"
DataPath="/home/csi20local/Dropbox/phd/Projects/Stanford/Data"
DataPath="/media/cs1623/Elements/portugal"
DataPath="/media/cs1623/Elements/Vitaliy"
DataPath="/media/cs1623/One Touch/Backup_April2023/Dropbox/phd/Projects/Stanford/Data/DICOM_Gated_CT"
f20_cases = ['21', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '34']
f20_cases = [f'CT-CRT/case{case_ind}' for case_ind in f20_cases]
ebr=['EBR/case01', 'EBR/case02']
f20_cases = f20_cases + ebr


def ReadFibreStrain(case, fibre_arch, frame, file_path):
	"""
	Read in fibre strain .txt file

	Arguments:
		* case
		* fibre_arch - e.g. endo_avg
		* frame - e.g. 4
	"""

	## Read in Fibre Strains
	strain_df = pd.read_csv(f'{DataPath}/{case}/{file_path}/{fibre_arch}-strains-t{frame}.txt', 
		sep=' ', skiprows=2, names=['f1', 'f2', 'f3'])

	return strain_df

def ReadFibreStrain_specify_initialframe(case, fibre_arch, initial_frame, later_frame, file_path):
	"""
	Read in fibre strain .txt file

	Arguments:
		* case
		* fibre_arch - e.g. endo_avg
		* frame - e.g. 4
	"""

	## Read in Fibre Strains
	strain_df = pd.read_csv(f'{DataPath}/{case}/{file_path}/{fibre_arch}-strains-t{initial_frame}-t{later_frame}.txt', 
		sep=' ', skiprows=2, names=['f1', 'f2', 'f3'])

	return strain_df

def CalcMeanRegionalStrain(strain_array, region, label_ar):

	"""
	strain_array should be array containing all strains, shape N_cells X 3 X 10
	label_ar should be array containing all region_labels for each cell

	region should be 
	1.0 roof
	2.0 sept
	3.0 lat
	4.0 ant
	5.0 post
	"""

	print("strain_array shape: ", strain_array.shape)
	## Filter array by region
	region_ar = strain_array[label_ar==region]
	print("region_ar shape: ", region_ar.shape)

	# print("strain_array shape: ", strain_array.shape)
	# ## Filter array by region
	# region_ar = strain_array[label_ar==region]
	# print("region_ar shape: ", region_ar.shape)

	print("region_ar_mean max: ", np.nanmax(region_ar))
	## Calculate mean regional strains
	region_ar_mean = np.nanmean(region_ar, axis=0)
	region_ar_mean = region_ar_mean*100.

	print("ar_mean shape: ", region_ar_mean.shape) ## should be ( 3, 10)

	return region_ar_mean

def CalcMeanGlobalStrain_excl_PVs(strain_array, label_ar):

	"""
	strain_array should be array containing all strains of shape: Num_cells X 3 X 10
	label_ar should be array containing all region_labels for each cell

	Removes region with label = 0.0
	"""

	## Filter array by region
	region_ar = strain_array[label_ar!=0.0]

	## Calculate mean regional strains
	region_ar_mean = np.nanmean(region_ar, axis=0)
	region_ar_mean = region_ar_mean*100.

	print("region_ar_mean shape: ", region_ar_mean.shape) ## should be ( 3, 10)

	return region_ar_mean


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Plot strain transients. This uses the percentiles filter step to filter out extreme positive values of fibre strain.')

	parser.add_argument('--case', required=True, help='case to plot strains for. e.g. CT-CRT/case01 or DICOMs/S-0400')
	parser.add_argument('--file-path', required=True, help='project directory containing all strain .txt files e.g. MT-HiRes/SW-0.0-BE-1e-9')
	parser.add_argument('--fibre-arch', required=True, help='fibre architecture to plot fibre strains for e.g. endo_avg')
	parser.add_argument('--numTimes', help='Total number of time frames [10]', default=10)
	parser.add_argument('--regional', action='store_true')
	parser.add_argument('--save-txt', action='store_true')
	parser.add_argument('--fibres-path', required=True, help='path to Fibres. e.g. dcm0/Fibres_HaoSeg or UAC_CT')

	args = parser.parse_args()

	## Read strains
	## ar dims: N_cells X N_strain_metrics (f1, f2, f3) X N_frames
	df = ReadFibreStrain(args.case, args.fibre_arch, 1, args.file_path)
	ar = np.zeros((df.shape[0], 3, args.numTimes))

	for i in range(1, args.numTimes):
		# print(i)
		ar[:, :, i] = ReadFibreStrain(args.case, args.fibre_arch, i, args.file_path).to_numpy()
		# ar[:, :, i] = ReadFibreStrain_specify_initialframe(args.case, args.fibre_arch, 5, i, args.file_path).to_numpy()

	## Read in 2D UAC and extract regional labels
	# uac_msh = pv.read(f"{DataPath}/{args.case}/{args.fibres_path}/LCoords_2D_R_v3_C-regional_labels.vtk")
	uac_msh = pv.read(f"{DataPath}/{args.case}/{args.fibres_path}/clean-Labelled-refined-aligned.vtp")
	region_label_ar = np.array(uac_msh.cell_data['region_label_v2'])
	# print("region_label_ar.shape ", region_label_ar.shape)

	## Scaled Jacobian filter
	## Read in mesh quality .txt file
	for i in range(1, args.numTimes):
		scal_jac = np.loadtxt(f"{DataPath}/{args.case}/{args.file_path}/cLr-fibres-aligned-{i}-scal_jacob-thr0.2.txt")

		## Check is scal_jac has same shape as df[0], should be number of cells
		if scal_jac.shape[0] != df.shape[0]:
			print("Check Scaled Jacobian and df shapes!")
		elif scal_jac.shape[0] == df.shape[0]:
			print("Scaled Jacobian and df shapes match!")
	
		## Remove elemental strains for poor quality elements
		msh_qual_thresh=0.2
		msh_qual_pass = scal_jac>msh_qual_thresh
		ar[~msh_qual_pass, :, i] = np.nan

	print("Max Element strain across time:",  np.nanmax(ar))
	print("Number of elemental strains ommitted across time: ", np.count_nonzero(np.isnan(ar)))

	if args.regional:
		print("Plotting regional strains!")

		## Testing adding region_label_ar to numpy array dimension
		roof_ar = ar[region_label_ar==1.0]
		print("ar shape: ", ar.shape)
		print("region_label_ar shape for 1.0 label: ", region_label_ar[region_label_ar==1.0].shape)
		print("roof_ar shape: ", roof_ar.shape)

		## Calculate regional strains
		roof_mean = CalcMeanRegionalStrain(ar, 1.0, region_label_ar)
		sept_mean = CalcMeanRegionalStrain(ar, 2.0, region_label_ar)
		lat_mean = CalcMeanRegionalStrain(ar, 3.0, region_label_ar)
		ant_mean = CalcMeanRegionalStrain(ar, 4.0, region_label_ar)
		post_mean = CalcMeanRegionalStrain(ar, 5.0, region_label_ar)

		if args.save_txt:
			print("saving txt files")
			## Save strains to .txt
			np.savetxt(f"{DataPath}/{args.case}/{args.file_path}/{args.fibre_arch}_excl_PVs_mshqual_meanstrains_roof.txt", roof_mean, fmt='%g')
			np.savetxt(f"{DataPath}/{args.case}/{args.file_path}/{args.fibre_arch}_excl_PVs_mshqual_meanstrains_sept.txt", sept_mean, fmt='%g')
			np.savetxt(f"{DataPath}/{args.case}/{args.file_path}/{args.fibre_arch}_excl_PVs_mshqual_meanstrains_lat.txt", lat_mean, fmt='%g')
			np.savetxt(f"{DataPath}/{args.case}/{args.file_path}/{args.fibre_arch}_excl_PVs_mshqual_meanstrains_ant.txt", ant_mean, fmt='%g')
			np.savetxt(f"{DataPath}/{args.case}/{args.file_path}/{args.fibre_arch}_excl_PVs_mshqual_meanstrains_post.txt", post_mean, fmt='%g')

		## First plot f1 only
		fig, (ax1) = plt.subplots(1,1,figsize=(7,5))

		normTime=np.arange(0, args.numTimes)/args.numTimes
		
		ax1.plot(normTime, roof_mean[0, :], label='roof', lw=2)
		ax1.plot(normTime, sept_mean[0, :], label='sept', lw=2)
		ax1.plot(normTime, lat_mean[0, :], label='lat', lw=2)
		ax1.plot(normTime, ant_mean[0, :], label='ant', lw=2)
		ax1.plot(normTime, post_mean[0, :], label='post', lw=2)
		ax1.set_title(f'Regional {args.fibre_arch} f1 strain')
		ax1.set(xlabel='Time (normalised)')
		ax1.set(ylabel='Fibre strain')
		ax1.label_outer()
		ax1.grid(True)

		ax1.legend()

		fig.savefig(f'{DataPath}/{args.case}/{args.file_path}/{args.fibre_arch}_excl_PVs_mshqual_regional_f1', dpi=200)

		# plt.show()

		## Second plot f2 only
		fig, (ax1) = plt.subplots(1,1,figsize=(7,5))

		normTime=np.arange(0, args.numTimes)/args.numTimes
		
		ax1.plot(normTime, roof_mean[1, :], label='roof', lw=2)
		ax1.plot(normTime, sept_mean[1, :], label='sept', lw=2)
		ax1.plot(normTime, lat_mean[1, :], label='lat', lw=2)
		ax1.plot(normTime, ant_mean[1, :], label='ant', lw=2)
		ax1.plot(normTime, post_mean[1, :], label='post', lw=2)
		ax1.set_title(f'Regional {args.fibre_arch} f2 strain')
		ax1.set(xlabel='Time (normalised)')
		ax1.set(ylabel='Fibre strain')
		ax1.label_outer()
		ax1.grid(True)

		ax1.legend()

		fig.savefig(f'{DataPath}/{args.case}/{args.file_path}/{args.fibre_arch}_excl_PVs_mshqual_regional_f2', dpi=200)

		# plt.show()

		## Third plot both
		prop_cycle = plt.rcParams['axes.prop_cycle']
		colors = prop_cycle.by_key()['color']

		fig, (ax1) = plt.subplots(1,1,figsize=(7,5))

		normTime=np.arange(0, args.numTimes)/args.numTimes
		
		ax1.plot(normTime, roof_mean[0, :], label='f1 roof', lw=2)
		ax1.plot(normTime, roof_mean[1, :], label='f2 roof', lw=2, ls='--', c=colors[0])
		ax1.plot(normTime, sept_mean[0, :], label='f1 sept', lw=2)
		ax1.plot(normTime, sept_mean[1, :], label='f2 sept', lw=2, ls='--', c=colors[1])
		ax1.plot(normTime, lat_mean[0, :], label='f1 lat', lw=2)
		ax1.plot(normTime, lat_mean[1, :], label='f2 lat', lw=2, ls='--', c=colors[2])
		ax1.plot(normTime, ant_mean[0, :], label='f1 ant', lw=2)
		ax1.plot(normTime, ant_mean[1, :], label='f2 ant', lw=2, ls='--', c=colors[3])
		ax1.plot(normTime, post_mean[0, :], label='f1 post', lw=2)
		ax1.plot(normTime, post_mean[1, :], label='f2 post', lw=2, ls='--', c=colors[4])
		ax1.set_title(f'Regional {args.fibre_arch} f1 & f2 strain')
		ax1.set(xlabel='Time (normalised)')
		ax1.set(ylabel='Fibre strain')
		ax1.label_outer()
		ax1.grid(True)

		ax1.legend()

		fig.savefig(f'{DataPath}/{args.case}/{args.file_path}/{args.fibre_arch}_excl_PVs_mshqual_regional', dpi=200)

		# plt.show()

	else:
		print("Plotting global strains!")

		## Calculate mean
		global_mean = CalcMeanGlobalStrain_excl_PVs(ar, region_label_ar)
		print(global_mean.shape)

		if args.save_txt:
			print("Saving txt files")
			## Save strains to .txt
			np.savetxt(f"{DataPath}/{args.case}/{args.file_path}/{args.fibre_arch}_excl_PVs_mshqual_meanstrains_global.txt", global_mean, fmt='%g')

		fig, (ax1) = plt.subplots(1,1,figsize=(7,5))

		normTime=np.arange(0, args.numTimes)/args.numTimes
		
		ax1.plot(normTime, global_mean[0, :], label='f1')
		ax1.plot(normTime, global_mean[1, :], label='f2')
		ax1.set_title(f'Global {args.fibre_arch} Fibre strain')
		ax1.set(xlabel='Time (normalised)')
		ax1.set(ylabel='Fibre strain')
		ax1.label_outer()
		ax1.grid(True)

		ax1.legend()

		fig.savefig(f'{DataPath}/{args.case}/{args.file_path}/{args.fibre_arch}_excl_PVs_mshqual_global.png', dpi=200)

		# plt.show()