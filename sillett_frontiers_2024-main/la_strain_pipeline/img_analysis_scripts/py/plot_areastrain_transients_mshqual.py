## Plots area strain transients for:

import matplotlib.pyplot as plt
import pandas as pd
import argparse
import numpy as np
import pyvista as pv

# Set DataPath for data location
# DataPath="/media/cs1623/Elements/Vitaliy"
# DataPath="/home/csi20/Data/Vitaliy"
# DataPath="/home/csi20/Data/VitaliyProject_Tiffany_Reproducibility"
DataPath="/home/csi20/Data/Vitaliy_Reproducibility"

f20_cases = ['21', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '34']
f20_cases = [f'CT-CRT/{case_ind}' for case_ind in f20_cases]
ebr=['EBR/case01', 'EBR/case02']
f20_cases = f20_cases + ebr

def ReadAreaStrain(case, frame, file_path):

	strain_df = pd.read_csv(f'{DataPath}/{case}/{file_path}/area-strains-{frame}.csv')

	return strain_df

def ReadAreaStrain_wrtConfig(case, frame, file_path, config_frame):

	strain_df = pd.read_csv(f'{DataPath}/{case}/{file_path}/area-strains-{frame}-wrt-t{config_frame}.csv')

	return strain_df

def ReadSQUEEZStrain(case, frame):

	if case in f20_cases:
		strain_df = pd.read_csv(f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9/squeez-{frame}.csv')

	else:
		strain_df = pd.read_csv(f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9/squeez-{frame}.csv')

	return strain_df

def CalcMeanRegionalStrain(df, region):

	"""
	df should be DataFrame containing all strains, with region label column

	region should be 
	1.0 roof
	2.0 sept
	3.0 lat
	4.0 ant
	5.0 post
	"""

	## Filter df by region
	df_filter = df[df['region'] == region]
	df_filter_drop = df_filter.drop(labels='region', axis=1)

	## Calculate mean regional strains
	series_mean = df_filter_drop.mean(axis=0)
	ar_mean = series_mean.to_numpy()
	ar_mean = ar_mean*100.

	print("ar_mean shape: ", ar_mean.shape) ## should be (10,)

	return ar_mean

def CalcMeanGlobalStrain_excl_PVs(df):

	"""
	df should be DataFrame containing all strains, with region label column

	Excludes region 0.0
	"""

	## Filter df by region
	df_filter = df[df['region'] != 0.0]
	df_filter_drop = df_filter.drop(labels='region', axis=1)

	## Calculate mean regional strains
	ar_mean = np.nanmean(df_filter_drop, axis=0)
	ar_mean = ar_mean*100.

	print("ar_mean shape: ", ar_mean.shape) ## should be (10,)

	return ar_mean

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Plot area strain transients. Excludes all but the LA body label for calculating mean strains.')

	parser.add_argument('--case', required=True, help='case to plot strains for e.g. CT-CRT/case01 or DICOMs/S-0400')
	parser.add_argument('--file-path', required=True, help='project directory containing all strain .txt files e.g. MT-HiRes/SW-0.0-BE-1e-9')
	parser.add_argument('--fibres-path', required=True, help='fibres project directory. e.g. dcm0/Fibres_HaoSeg or UAC_CT')
	parser.add_argument('--numTimes', help='Total number of time frames [10]', default=10)
	parser.add_argument('--regional', action='store_true')
	parser.add_argument('--squeez', action='store_true')
	parser.add_argument('--save-txt', action='store_true')
	parser.add_argument('--data-path')

	args = parser.parse_args()

	## Distinguish between area and squeez strain metrics
	if args.squeez:
		print("Calculating SQUEEZ strain!")

		strain_type = 'squeez'

		## Read squeez strains
		df = ReadSQUEEZStrain(args.case, 1)
		ar = np.zeros((df.shape[0], args.numTimes))

		for i in range(1, args.numTimes):
			# print(i)
			df = ReadSQUEEZStrain(args.case, i)
			ar[:, i] = df['Area'].to_numpy()

		ar = ar - 1.
		ar[:, 0] = 0.
	
	else:
		print("Calculating Area strain!")

		strain_type = 'area'

		## Read area strains
		df = ReadAreaStrain(args.case, 1, args.file_path)
		ar = np.zeros((df.shape[0], int(args.numTimes)))

		for i in range(1, int(args.numTimes)):
			# print(i)
			df = ReadAreaStrain(args.case, i, args.file_path)
			ar[:, i] = df['Area'].to_numpy()

		## Jacobian Quality Check
		for i in range(1, int(args.numTimes)):
			scal_jac = np.loadtxt(f"{DataPath}/{args.case}/{args.file_path}/cLr-fibres-aligned-{i}-scal_jacob-thr0.2.txt")

			## Check is scal_jac has same shape as df[0], should be number of cells
			if scal_jac.shape[0] != df.shape[0]:
				print("Check Scaled Jacobian and df shapes!")
			elif scal_jac.shape[0] == df.shape[0]:
				print("Scaled Jacobian and df shapes match!")

			## Remove elemental strains for poor quality elements
			msh_qual_thresh=0.2
			msh_qual_pass = scal_jac>msh_qual_thresh
			ar[~msh_qual_pass, i] = np.nan

	## Print number of nan elements
	print("Number of elemental strains ommitted across time: ", np.count_nonzero(np.isnan(ar)))

	## Read in 2D UAC to extract regional labels
	uac_msh = pv.read(f"{DataPath}/{args.case}/{args.fibres_path}/clean-Labelled-refined-aligned.vtp")
	region_label_ar = np.array(uac_msh.cell_data['region_label_v2'])
	
	## Master dataframe, append region labels as a column
	df_master = pd.DataFrame(data=ar)
	df_master['region'] = region_label_ar

	if args.regional:
		print("Plotting regional strains")

		## Calculate regional strains
		roof_mean = CalcMeanRegionalStrain(df_master, 1.0)
		sept_mean = CalcMeanRegionalStrain(df_master, 2.0)
		lat_mean = CalcMeanRegionalStrain(df_master, 3.0)
		ant_mean = CalcMeanRegionalStrain(df_master, 4.0)
		post_mean = CalcMeanRegionalStrain(df_master, 5.0)

		## savetxt
		if args.save_txt:
			print("Saving regional strains.")
			np.savetxt(f'{DataPath}/{args.case}/{args.file_path}/{strain_type}_meanstrains_roof_excl_PVs_mshqual.txt', roof_mean)
			np.savetxt(f'{DataPath}/{args.case}/{args.file_path}/{strain_type}_meanstrains_sept_excl_PVs_mshqual.txt', sept_mean)
			np.savetxt(f'{DataPath}/{args.case}/{args.file_path}/{strain_type}_meanstrains_lat_excl_PVs_mshqual.txt', lat_mean)
			np.savetxt(f'{DataPath}/{args.case}/{args.file_path}/{strain_type}_meanstrains_ant_excl_PVs_mshqual.txt', ant_mean)
			np.savetxt(f'{DataPath}/{args.case}/{args.file_path}/{strain_type}_meanstrains_post_excl_PVs_mshqual.txt', post_mean)

		# Make figure
		fig, (ax1) = plt.subplots(1,1,figsize=(7,5))

		normTime=np.arange(0, int(args.numTimes))/int(args.numTimes)

		ax1.plot(normTime, roof_mean, label='roof', linewidth=2)
		ax1.plot(normTime, sept_mean, label='sept', linewidth=2)
		ax1.plot(normTime, lat_mean, label='lat', linewidth=2)
		ax1.plot(normTime, ant_mean, label='ant', linewidth=2)
		ax1.plot(normTime, post_mean, label='post', linewidth=2)

		if args.squeez:
			ax1.set_title(f'Regional SQUEEZ Strain')
		else:
			ax1.set_title(f'Regional Area Strain')

		ax1.set(xlabel='Time (normalised)')
		ax1.set(ylabel='Area strain')
		ax1.label_outer()
		ax1.grid(True)

		ax1.legend()

		fig.savefig(f'{DataPath}/{args.case}/{args.file_path}/{strain_type}_strains_regional_excl_PVs_mshqual.png', dpi=200)

		# plt.show()

	else:
		print("Plotting global strains")

		## Calculate mean global strain
		global_mean = CalcMeanGlobalStrain_excl_PVs(df_master)
		print(global_mean.shape)

		if args.save_txt:
			print("Saving global strains")
			np.savetxt(f'{DataPath}/{args.case}/{args.file_path}/{strain_type}_meanstrains_global_excl_PVs_mshqual.txt', global_mean)

		# Make figure

		fig, (ax1) = plt.subplots(1,1,figsize=(7,5))

		normTime=np.arange(0, int(args.numTimes))/int(args.numTimes)
		
		ax1.plot(normTime, global_mean)

		if args.squeez:
			ax1.set_title(f'Global SQUEEZ Strain')
		else:
			ax1.set_title(f'Global Area Strain')

		ax1.set(xlabel='Time (normalised)')
		ax1.set(ylabel='Area strain')
		ax1.label_outer()
		ax1.grid(True)

		fig.savefig(f'{DataPath}/{args.case}/{args.file_path}/{strain_type}_strains_global_excl_PVs_mshqual.png', dpi=200)

		# plt.show()