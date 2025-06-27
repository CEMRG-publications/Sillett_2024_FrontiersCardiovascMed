import pandas as pd
import pyvista as pv
import numpy as np

DataPath="/home/csi20local/Dropbox/phd/Data/RG_CT_Cases"

f20_cases = ['21', '23', '26', '28', '29', '31']
f20_cases = [f'CT-CRT-{case_ind}' for case_ind in f20_cases]

def ReadAreas(case, msh_name):
	"""
	Read areas.txt file of a given msh 

	Arguments:
		* case
		* msh_name e.g. cLr-fibres-refined-4
	"""
	if case in f20_cases:
		area_df = pd.read_csv(f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9/{msh_name}-areas.txt', sep=' ', 
			names=['Cell', 'Cell_Id', 'Label', 'Area'], skiprows=1)

	else:
		area_df = pd.read_csv(f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9/{msh_name}-areas.txt', sep=' ', 
			names=['Cell', 'Cell_Id', 'Label', 'Area'], skiprows=1)

	return area_df

def ReadFibreStrain(case, fibre_arch, frame):
	"""
	Read in fibre strain .txt file

	Arguments:
		* case
		* fibre_arch - e.g. endo_avg
		* frame - e.g. 4
	"""

	## Read in Fibre Strains
	if case in f20_cases:

		strain_df = pd.read_csv(f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9/{fibre_arch}-strains-t{frame}.txt', 
    		sep=' ', skiprows=2, names=['f1', 'f2', 'f3'])

	else:
		strain_df = pd.read_csv(f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9/{fibre_arch}-strains-t{frame}.txt', 
    		sep=' ', skiprows=2, names=['f1', 'f2', 'f3'])

	return strain_df

def ReadAreaStrain(case, frame):

	if case in f20_cases:
		strain_df = pd.read_csv(f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9/area-strains-{frame}.csv')

	else:
		strain_df = pd.read_csv(f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9/area-strains-{frame}.csv')

	return strain_df

def ReadSQUEEZStrain(case, frame):

	if case in f20_cases:
		strain_df = pd.read_csv(f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9/squeez-{frame}.csv')

	else:
		strain_df = pd.read_csv(f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9/squeez-{frame}.csv')

	return strain_df

def ReadMeanStrainCurves(case, strain_type, region):
	"""
	Function to read in mean strain curves

	Arguments:
		* case: e.g. CT-CRT-01
		* strain_type: either fibre architecture or area/squeez
		* region: either global or one of the 5 regions (roof, sept, lat, ant, post) 
	"""

	## Set tracking path
	if case in f20_cases:
		trackingPath = f'{DataPath}/{Case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9'
	else:
		trackingPath = f'{DataPath}/{Case}/MT-HiRes/SW-0.0-BE-1e-9'

	ans = np.loadtxt(f'{trackingPath}/{strain_type}_meanstrains_{region}.txt')
	return ans

def GlobalAkineticFraction(case, threshold, fibre_arch, fibre_component):
    
    ## Read in Fibre Strains
    strain_df = ReadFibreStrain(case, fibre_arch, '4')
      
    ## Read in Areas
    area_df = ReadAreas(case, 'cLr-fibres-aligned-4')
        
    ## Apply threshold
    thresh_df = area_df[(strain_df[f'{fibre_component}'] < threshold) & (strain_df[f'{fibre_component}'] > -threshold)]
    
    # Find Akinetic and Total areas
    akin_area = thresh_df['Area'].sum()
    tot_area = area_df['Area'].sum()
    
    # Find akinetic fraction
    akin_frac = akin_area/tot_area
    
    return akin_frac

def GlobalAkineticFraction_Area(case, threshold):
    
    ## Read in Area Strains
    strain_df = ReadAreaStrain(case, '4')
      
    ## Read in Areas
    area_df = ReadAreas(case, 'cLr-fibres-aligned-4')
        
    ## Apply threshold
    thresh_df = area_df[(strain_df['Area'] < threshold) & (strain_df['Area'] > -threshold)]
    
    # Find Akinetic and Total areas
    akin_area = thresh_df['Area'].sum()
    tot_area = area_df['Area'].sum()
    
    # Find akinetic fraction
    akin_frac = akin_area/tot_area
    
    return akin_frac

def Generate_Region_Labels(case):

	## Read in 2D UAC and LA msh
	uac_msh = pv.read(f"{DataPath}/{case}/dcm0/Fibres/Labelled_Coords_2D_Rescaling_v3_C.vtk")
	la_msh = pv.read(f"{DataPath}/{case}/dcm0/Fibres/clean-Labelled-refined.vtk")

	## Get upper/lower RH/LH bounds
	## extract veins
	lipv = uac_msh.extract_cells(uac_msh['data']==13)
	rspv = uac_msh.extract_cells(uac_msh['data']==15)

	## bounds
	lower_bound = lipv.center[1] ## ymin
	left_bound = lipv.center[0]  ## xmax

	upper_bound = rspv.center[1]  ## ymax
	right_bound = rspv.center[0]  ## xmin

	## Get region cell IDs
	roof_inds = uac_msh.find_cells_within_bounds([right_bound, left_bound, lower_bound, upper_bound, 0.0, 0.0])
	lat_inds = uac_msh.find_cells_within_bounds([left_bound, 1.0, 0.0, 1.0, 0.0, 0.0])
	sept_inds = uac_msh.find_cells_within_bounds([0.0, right_bound, 0.0, 1.0, 0.0, 0.0])
	post_inds = uac_msh.find_cells_within_bounds([right_bound, left_bound, 0.0, lower_bound, 0.0, 0.0])
	ant_inds = uac_msh.find_cells_within_bounds([right_bound, left_bound, upper_bound, 1.0, 0.0, 0.0])

	## Append cell_data to 2D UAC and LA msh
	local_region_ar = np.zeros((uac_msh.number_of_cells,))

	local_region_ar[roof_inds] = 1.0
	local_region_ar[sept_inds] = 2.0
	local_region_ar[lat_inds] = 3.0
	local_region_ar[ant_inds] = 4.0
	local_region_ar[post_inds] = 5.0

	uac_msh.cell_data["region_label"] = local_region_ar
	la_msh.cell_data["region_label"] = local_region_ar

	## Save mshes
	uac_msh.save(f"{DataPath}/{case}/dcm0/Fibres/LCoords_2D_R_v3_C-regional_labels.vtk")
	la_msh.save(f"{DataPath}/{case}/dcm0/Fibres/cLr-regional_labels.vtk")