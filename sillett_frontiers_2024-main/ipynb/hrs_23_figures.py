## Scripts for generating figures for hrs 23 absract

## Libraries used
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyvista as pv

##################################################################################################################################################################################################
######################################################################################## Global variables ########################################################################################
##################################################################################################################################################################################################

numTimes = 10
nTime=np.arange(0, numTimes)/numTimes

DataPath="/home/csi20/Dropbox/phd/Data/RG_CT_Cases"
# DataPath="/media/csi20local/Seagate Portable Drive/Master/Data/RG_CT_Cases"

f20_cases = ['21', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '34']
f20_cases = [f'CT-CRT/case{case_ind}' for case_ind in f20_cases]
ebr=['1', '2', '4', '5', '6']
ebr=[f'EBR/case0{i}' for i in ebr]
f20_cases = f20_cases + ebr

## Kiru demographics update
## Removed 18 ue to imaging rhythm
nonaf_cases = ['02', '05', '06', '07', '08', '09', '10', '12', '14',
             '15', '16', '17', '24', '28', '29', '30', '32', '34']
nonaf_cases = [f"CT-CRT/case{case}" for case in nonaf_cases]
nonaf_cases = nonaf_cases + ebr[-3:]

## Kiru update
## Removed 21 25 due to imaging rhtyhm
af_cases = ['01', '19', '20', '23', '26', '27', '31']
af_cases = [f'CT-CRT/case{case}' for case in af_cases]
af_cases = af_cases + ebr[:2]

Fibres_nHaoSeg_list = ['21', '23', '24', '25', '26', '27', '28', '29', '30', '31']
Fibres_nHaoSeg_list = [f'CT-CRT/case{case}' for case in Fibres_nHaoSeg_list]

AF_rhythm_cases = ['18', '25', '31']
AF_rhythm_cases = ['18', '19', '23', '25', '26', '27', '31']
AF_rhythm_cases = [f"CT-CRT/case{case}" for case in AF_rhythm_cases]

nonaf_cases_omit_AF = [case for case in nonaf_cases if case not in AF_rhythm_cases]
af_cases_omit_AF = [case for case in af_cases if case not in AF_rhythm_cases]

## Vxm training folds
test_fold1 = ['06', '08', '14', '28', '29']
test_fold1 = [f"CT-CRT/case{case}" for case in test_fold1]

test_fold2 = ['01', '16', '20', '25']
test_fold2 = [f"CT-CRT/case{case}" for case in test_fold2]
test_fold2.append("EBR/case02")

test_fold3 = ['05', '18', '19', '30', '34']
test_fold3 = [f"CT-CRT/case{case}" for case in test_fold3]

test_fold4 = ['07', '10', '17', '21']
test_fold4 = [f"CT-CRT/case{case}" for case in test_fold4]
test_fold4.append("EBR/case01")

test_fold5 = ['09', '12', '24', '27', '31']
test_fold5 = [f"CT-CRT/case{case}" for case in test_fold5]

test_fold6 = ['02', '15', '23', '26', '32']
test_fold6 = [f"CT-CRT/case{case}" for case in test_fold6]

new_cases = np.arange(4,7,1)
new_cases = [f"EBR/case0{case}" for case in new_cases]

## Old AF-nonAF splits

# ## nAF
# nonaf_cases = ['01', '02', '05', '06', '07', '08', '09', '12', '14',
#              '15', '16', '17', '18', '24', '27', '28', '29', '30',
#              '32']
# nonaf_cases = [f"CT-CRT/case{case}" for case in nonaf_cases]

# ## Ronak update on demograhpics
# nonaf_cases = ['01', '02', '05', '06', '07', '08', '09', '12', '14',
#              '15', '16', '17', '24', '28', '29', '30', '32']
# nonaf_cases = [f"CT-CRT/case{case}" for case in nonaf_cases]

# # AF
# af_cases = ['10', '19', '20', '23', '26', '31', '25', '34']
# af_cases = [f'CT-CRT/case{case}' for case in af_cases]

# ## Ronak update on demographics
# af_cases = ['10', '18', '19', '20', '23', '26', '27', '31', '25', '34']
# af_cases = [f'CT-CRT/case{case}' for case in af_cases]
# af_cases = af_cases + ebr


##################################################################################################################################################################################################
########################################################################################### Functions ############################################################################################
##################################################################################################################################################################################################

######################################################################################## Plotting ################################################################################################

def plot_area_strain(ax, case, label, strain_type, region):
    
    """
    Previously called plot_strain().

    Use to plot area and squeez strains.
    Usage:
        * ax: axis to plot on
        * case: case
        * label: label for curve
        * strain_type: either area or squeez
        * region: global, roof, lat, sept, ant, post
    """
    
    if case in f20_cases:
        filepath=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9'
    
    else:
        filepath=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9'
    
    ## area or squeez
    data = np.loadtxt(f'{filepath}/{strain_type}_meanstrains_{region}_excl_PVs.txt')
    ax.plot(nTime, data, label=label)

def plot_fibre_strains(ax, case, label, fibre_arch, component, region, linestyle='solid', color='b'):
    """
    Use this function to plot fibre strains.
    Usage:
        * ax: axis to plot on
        * case: case
        * label: label for curve
        * fibre_arch: endo_avg, epi_avg
        * component: 0 (along fibres), 1 (across fibres), 2 (normal)
        * region: global, ant, lat, post, roof, sept
        * linestyle: ls to use [deafult: solid]
        * color: color [default: blue]
    """
    
    ## retrieve data
    data = retrieve_fibres_data(case, fibre_arch, component, region)
    
    ## plot
    ax.plot(nTime, data, label=label, ls=linestyle)

######################################################################################## Retrieving Data ###########################################################################################

def retrieve_area_strain_all_data(case, strain_type, time_frame):
    """
    This function reads in all cell's area or squeez strains

    Usage:
        * case: case e.g. CT-CRT/case01
        * strain_type: either 'area' or 'squeez'
        * time_frame: between 1 and 9
    """

    if case in f20_cases:
        filepath=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9'

    else:
        filepath=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9'

    if strain_type == 'area':
        data = pd.read_csv(f"{filepath}/{strain_type}-strains-{time_frame}.csv")

    else: ## squeez
        data = pd.read_csv(f"{filepath}/{strain_type}-{time_frame}.csv")        

    return data

def retrieve_fibre_strain_all_data(case, fibre_arch, time_frame):
    """
    This function reads in all cells' fibre strains.
    Previously called retrieve_fibres_all_data

    Usage:
        * case 
        * fibre_arch: e.g. endo_avg
        * time_frame: between 1 and 9
    """

    if case in f20_cases:
        filepath=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9'

    else:
        filepath=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9'


    data = pd.read_csv(f"{filepath}/{fibre_arch}-strains-t{time_frame}.txt", 
        names=["f1", "f2", "f3"], skiprows=2, sep=' ')

    return data

def retrieve_area_strain_transient(case, strain_type, region):
    """
    Use this function to retrieve global and regional area/squeez strain transients.
    Previously called retrieve_area_data.

    Transients exclude LAA and PVs strains.

    Usage:
        * case: case
        * strain_type: 'area' or 'squeez'
        * region: 'global', 'roof', 'lat', 'sept', 'ant', 'post'
    """
    
    if case in f20_cases:
        filepath=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9'
    
    else:
        filepath=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9'
        
    data = np.loadtxt(f'{filepath}/{strain_type}_meanstrains_{region}_excl_PVs.txt')
    
    return data

def retrieve_area_strain_transient_Vxm(case, strain_type, region):
    """
    Use this function to retrieve global and regional area/squeez strain transients.
    Previously called retrieve_area_data.

    Transients exclude LAA and PVs strains.

    Usage:
        * case: case
        * strain_type: 'area' or 'squeez'
        * region: 'global', 'roof', 'lat', 'sept', 'ant', 'post'
    """
    
    if case in test_fold1:
        filepath=f'{DataPath}/{case}/Vxm/30_case/opt_train/train_fold1/lambda_20e-2_lr3e-4'

    elif case in test_fold2:
        filepath=f'{DataPath}/{case}/Vxm/30_case/opt_train/train_fold2/lambda_20e-2_lr3e-4'        

    elif case in test_fold3:
        filepath=f'{DataPath}/{case}/Vxm/30_case/opt_train/train_fold3/lambda_20e-2_lr3e-4'

    elif case in test_fold4:
        filepath=f'{DataPath}/{case}/Vxm/30_case/opt_train/train_fold4/lambda_20e-2_lr3e-4'

    elif case in test_fold5:
        filepath=f'{DataPath}/{case}/Vxm/30_case/opt_train/train_fold5/lambda_20e-2_lr3e-4'

    elif case in test_fold6:
        filepath=f'{DataPath}/{case}/Vxm/30_case/opt_train/train_fold6/lambda_20e-2_lr3e-4'
    
    elif case in new_cases:
        filepath=f'{DataPath}/{case}/Vxm'

    data = np.loadtxt(f'{filepath}/{strain_type}_meanstrains_{region}_excl_PVs.txt')
    
    return data

def retrieve_fibre_strain_transient(case, fibre_arch, component, region):
    """
    Use this function to retrieve global and regional fibre strain transients.
    Previously called retrieve_fibres_data.

    Excludes LAA and PVs strains.
    Applies percentiles to omit extreme high valued cell fibre strains.

    Usage:
        * fibre_arch: endo_avg, epi_avg
        * component: 0 (along fibres), 1 (across fibres), 2 (normal)
        * region: global, ant, lat, post, roof, sept
    """
    
    if case in f20_cases:
        # filepath=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9'
        filepath=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9/percent_regional_strains'
    
    else:
        # filepath=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9'
        filepath=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9/percent_regional_strains'
        
    data = np.loadtxt(f'{filepath}/{fibre_arch}_excl_PVs_percent_meanstrains_{region}.txt')[component]
    
    return data

def retrieve_fibre_strain_transient_Vxm(case, fibre_arch, component, region):
    """
    Use this function to retrieve global and regional fibre strain transients created from Vxm FT.
    
    Excludes LAA and PVs strains.
    Applies percentiles to omit extreme high valued cell fibre strains.

    Usage:
        * fibre_arch: endo_avg, epi_avg
        * component: 0 (along fibres), 1 (across fibres), 2 (normal)
        * region: global, ant, lat, post, roof, sept
    """
    
    if case in test_fold1:
        filepath=f'{DataPath}/{case}/Vxm/30_case/opt_train/train_fold1/lambda_20e-2_lr3e-4'

    elif case in test_fold2:
        filepath=f'{DataPath}/{case}/Vxm/30_case/opt_train/train_fold2/lambda_20e-2_lr3e-4'        

    elif case in test_fold3:
        filepath=f'{DataPath}/{case}/Vxm/30_case/opt_train/train_fold3/lambda_20e-2_lr3e-4'

    elif case in test_fold4:
        filepath=f'{DataPath}/{case}/Vxm/30_case/opt_train/train_fold4/lambda_20e-2_lr3e-4'

    elif case in test_fold5:
        filepath=f'{DataPath}/{case}/Vxm/30_case/opt_train/train_fold5/lambda_20e-2_lr3e-4'

    elif case in test_fold6:
        filepath=f'{DataPath}/{case}/Vxm/30_case/opt_train/train_fold6/lambda_20e-2_lr3e-4'
        
    data = np.loadtxt(f'{filepath}/{fibre_arch}_excl_PVs_meanstrains_{region}.txt')[component]
    
    return data

def retrieve_fibre_strain_transient_local(case, fibre_arch, component, region):
    """
    Use this function to retrieve regional fibre strain transients for data on csi20local, and not on Dropbox.

    Excludes LAA and PVs strains.
    Applies percentiles to omit extreme high valued cell fibre strains.

    Usage:
        * fibre_arch: endo_avg, epi_avg
        * component: 0 (along fibres), 1 (across fibres), 2 (normal)
        * region: global, ant, lat, post, roof, sept
    """
    LocalDataPath="/home/csi20local/Data/RG_CT_Cases"
    
    if case in f20_cases:
        # filepath=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9'
        filepath=f'{LocalDataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9/percent_regional_strains'
    
    else:
        # filepath=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9'
        filepath=f'{LocalDataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9/percent_regional_strains'
        
    data = np.loadtxt(f'{filepath}/{fibre_arch}_excl_PVs_percent_meanstrains_{region}.txt')[component]
    
    return data

def area_strain_range(case, strain_type, region):
    """
    Use this function to retrieve range of global and regional area strain transient. Represents reservoir strain.

    Excludes LAA & PVs strains

    Usage:
        * strain_type: area, squeez
        * region: global, ant, lat, post, roof, sept
    """
        
    data = retrieve_area_strain_transient(case=case, strain_type=strain_type, region=region)
    data_range = np.ptp(data)
    
    return data_range

def area_strain_range_Vxm(case, strain_type, region):
    """
    Use this function to retrieve range of global and regional area strain transient using Vxm FT. Represents reservoir strain.

    Excludes LAA & PVs strains

    Usage:
        * strain_type: area, squeez
        * region: global, ant, lat, post, roof, sept
    """
        
    data = retrieve_area_strain_transient_Vxm(case=case, strain_type=strain_type, region=region)
    data_range = np.ptp(data)
    
    return data_range

def fibre_strain_range(case, fibre_arch, component, region):
    """
    Use this function to retrieve range of strain transients for fibre strains.
    Previously called data_range_fibres

    Excludes LAA & PVs strains
    Uses data from retrieve_fibre_strain_transient function which applies percentiles.

    Usage:
        * case: case
        * fibre_arch: endo_avg, epi_avg
        * component: 0, 1, 2
        * region: global, ant, lat, post, roof, sept 
    """
    
    data = retrieve_fibre_strain_transient(case=case, fibre_arch=fibre_arch, component=component, region=region)
    data_range = np.ptp(data)
    
    return data_range

def fibre_strain_range_Vxm(case, fibre_arch, component, region):
    """
    Use this function to retrieve range of strain transients for fibre strains created using Vxm FT

    Excludes LAA & PVs strains
    Uses data from retrieve_fibre_strain_transient function which applies percentiles.

    Usage:
        * case: case
        * fibre_arch: endo_avg, epi_avg
        * component: 0, 1, 2
        * region: global, ant, lat, post, roof, sept 
    """
    
    data = retrieve_fibre_strain_transient_Vxm(case=case, fibre_arch=fibre_arch, component=component, region=region)
    data_range = np.ptp(data)
    
    return data_range

def retrieve_fibre_strain_region(case, fibre_arch, time_frame, region, longitudinal=False):
	"""
	This function reads in all cells' fibre strains for a given region.
    Previously called extract_region

	Usage:
		* case 
		* fibre_arch: e.g. endo_avg
		* time_frame: between 1 and 9
		* long: if true, return local longitudinal strains, default is False
		* region: 
				* roof 1.0
				* sept 2.0
				* lat 3.0
				* ant 4.0
				* post 5.0
	"""

	if case in Fibres_nHaoSeg_list:
		filepath=f"/home/csi20/Dropbox/phd/Data/RG_CT_Cases/{case}/dcm0/Fibres/cLr-regional_labels.vtk"

	else:
		filepath=f"/home/csi20/Dropbox/phd/Data/RG_CT_Cases/{case}/dcm0/Fibres_HaoSeg/cLr-regional_labels.vtk"

	msh = pv.read(filepath)
	region_ar = np.array(msh.cell_data["region_label_v2"])

	condition = region_ar == region

	if case in f20_cases:
		filepath=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9'

	else:
		filepath=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9'

	if longitudinal:
		data = pd.read_csv(f"{filepath}/local_long_strain-{time_frame}.txt", 
			names=["f1", "f2", "f3"], skiprows=2, sep=' ')

	else:
		data = pd.read_csv(f"{filepath}/{fibre_arch}-strains-t{time_frame}.txt", 
			names=["f1", "f2", "f3"], skiprows=2, sep=' ')

	data = data[condition]

	return data

def retrieve_area_strain_region(case, strain_type, time_frame, region):
    """
    This function reads in all cells' area strains for a given region.
    Previously called extract_region_area.

    Usage:
        * case 
        * strain_type: 'area' or 'squeez'
        * time_frame: between 1 and 9
        * region: 
                * roof 1.0
                * sept 2.0
                * lat 3.0
                * ant 4.0
                * post 5.0
    """

    if case in Fibres_nHaoSeg_list:
        filepath=f"/home/csi20/Dropbox/phd/Data/RG_CT_Cases/{case}/dcm0/Fibres/cLr-regional_labels.vtk"

    else:
        filepath=f"/home/csi20/Dropbox/phd/Data/RG_CT_Cases/{case}/dcm0/Fibres_HaoSeg/cLr-regional_labels.vtk"

    msh = pv.read(filepath)
    region_ar = np.array(msh.cell_data["region_label_v2"])

    condition = region_ar == region

    if case in f20_cases:
        filepath=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9'

    else:
        filepath=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9'

    if strain_type=='area':
        data = pd.read_csv(f"{filepath}/{strain_type}-strains-{time_frame}.csv")

    else: ## squeez
        data = pd.read_csv(f"{filepath}/{strain_type}-{time_frame}.csv")

    data = data[condition]

    return data

def get_tsffd_trackingpath(case):
    """
    Use this function to get TSFFD tracking path

    Usage:
        * case: case
    """
    
    if case in f20_cases:
        ans=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9'

    else:
        ans=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9'        
    
    return ans

def get_vxm_trackingpath(case):
    """
    Use this function to get Vxm tracking path.

    Usage:
        * case: case
    """
    
    if case in test_fold1:
        filepath=f'{DataPath}/{case}/Vxm/30_case/opt_train/train_fold1/lambda_20e-2_lr3e-4'

    elif case in test_fold2:
        filepath=f'{DataPath}/{case}/Vxm/30_case/opt_train/train_fold2/lambda_20e-2_lr3e-4'        

    elif case in test_fold3:
        filepath=f'{DataPath}/{case}/Vxm/30_case/opt_train/train_fold3/lambda_20e-2_lr3e-4'

    elif case in test_fold4:
        filepath=f'{DataPath}/{case}/Vxm/30_case/opt_train/train_fold4/lambda_20e-2_lr3e-4'

    elif case in test_fold5:
        filepath=f'{DataPath}/{case}/Vxm/30_case/opt_train/train_fold5/lambda_20e-2_lr3e-4'

    elif case in test_fold6:
        filepath=f'{DataPath}/{case}/Vxm/30_case/opt_train/train_fold6/lambda_20e-2_lr3e-4'
    
    elif case in new_cases:
        filepath=f'{DataPath}/{case}/Vxm'
   
    return filepath