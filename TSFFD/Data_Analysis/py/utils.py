"""
This script contains useful functions for LA Tracking data analysis
"""

import os
import numpy as np

DataPath="/home/csi20local/Dropbox/phd/Data/RG_CT_Cases"
DataPath="/media/cs1623/One Touch/Backup_April2023/Dropbox/phd/Projects/Stanford/Data/DICOM_Gated_CT"
DataPath="/media/cs1623/Elements/Vitaliy"
DataPath="/media/cs1623/Elements1/Vitaliy_BiV"
DataPath="/media/cs1623/Elements/Vitaliy_BiV"
# DataPath="/home/csi20/Data/Vitaliy"
DataPath="/home/csi20/Data/Vitaliy_Reproducibility"
DataPath="/home/csi20/Data/VitaliyProject_Tiffany_Reproducibility"

# regions=['global', 'roof', 'lat', 'sept', 'ant', 'post']
regions=['global', 'roof', 'sept', 'lat', 'ant', 'post']

f20_cases = ['21', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '34']
f20_cases = [f'CT-CRT/case{case_ind}' for case_ind in f20_cases]
ebr=['1', '2', '4', '5', '6']
ebr=[f'EBR/case0{i}' for i in ebr]
f20_cases = f20_cases + ebr

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

def retrieve_final_ind(case, laptop=False):

    """
    Get index of point where notch is. Firstly tries notch from global strain transient, and then global volume transient.

    WIP.
    """

    if laptop:
        print("On bioeng347-lap!")
        home_dir="/home/csi20local"
    else:
        print("Not on laptop!")
        home_dir="/home/csi20"

    if ((case[0] == "E") or (case[0] == "C")):
        print("GSTT cohort")
        DataPath="/home/csi20/Dropbox/phd/Data/RG_CT_Cases"
        if case in f20_cases:
            filepath=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9'
        
        else:
            filepath=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9'
    
    elif case[0]=='S':
        print("Stanford cohort")
        DataPath="/home/csi20/Data/Stanford"
        DataPath="/media/cs1623/One Touch/Backup_April2023/Dropbox/phd/Projects/Stanford/Data/DICOM_Gated_CT"

        filepath=f'{DataPath}/{case}/MT/SW-0.0-BE-1e-9'
        final_ind_def_path=f"{filepath}/area_global_final_ind.txt"
        final_ind_vol_path=f"{filepath}/area_global_vol_final_ind.txt"

    elif case[0]=='P':
        print("Portugal cohort")

        final_ind_def_path=f"{home_dir}/Data/portugal/{case}/MT/SW-0.0-BE-1e-9/area_global_final_ind.txt"
        final_ind_vol_path=f"{home_dir}/Data/portugal/{case}/MT/SW-0.0-BE-1e-9/area_global_vol_final_ind.txt"
    
    elif case[0]=='V':
        print("Vitaliy cohort")
    
        final_ind_def_path=f"{home_dir}/Data/Vitaliy/{case}/LA/MT/SW-0.0-BE-1e-9/area_global_final_ind.txt"
        final_ind_vol_path=f"{home_dir}/Data/Vitaliy/{case}/LA/MT/SW-0.0-BE-1e-9/area_global_vol_final_ind.txt"

        final_ind_def_path=f"/media/cs1623/Elements/Vitaliy/{case}/LA/MT/SW-0.0-BE-1e-9/area_global_final_ind.txt"
        final_ind_vol_path=f"/media/cs1623/Elements/Vitaliy/{case}/LA/MT/SW-0.0-BE-1e-9/area_global_vol_final_ind.txt"

        final_ind_def_path=f"/media/cs1623/Elements/Vitaliy_BiV/{case}/LA/MT/SW-0.0-BE-1e-9/area_global_final_ind.txt"
        final_ind_vol_path=f"/media/cs1623/Elements/Vitaliy_BiV/{case}/LA/MT/SW-0.0-BE-1e-9/area_global_vol_final_ind.txt"

    if os.path.isfile(final_ind_def_path):
        print("File using default path exists")
        
        final_ind=np.loadtxt(final_ind_def_path)
        final_ind=int(final_ind)
        
        print("final ind", final_ind, "\n")

    elif os.path.isfile(final_ind_vol_path):
        print("File using vol path exists")
        
        final_ind=np.loadtxt(final_ind_vol_path)
        final_ind=final_ind/2.0
        final_ind=int(final_ind)
        
        print("final ind", final_ind, "\n")
    
    else:
        print("Neither file exists\n")
        final_ind=np.nan

    return final_ind

def retrieve_final_ind_20f(case, laptop=False):

    """
    Get index of point where notch is. Firstly tries notch from global strain transient, and then global volume transient.

    WIP.
    """

    if laptop:
        print("On bioeng347-lap!")
        home_dir="/home/csi20local"
    else:
        print("Not on laptop!")
        home_dir="/home/csi20"

    if ((case[0] == "E") or (case[0] == "C")):
        print("GSTT cohort")
        DataPath="/home/csi20/Dropbox/phd/Data/RG_CT_Cases"
        if case in f20_cases:
            filepath=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9'
        
        else:
            filepath=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9'
    
    elif case[0]=='S':
        print("Stanford cohort")
        DataPath="/home/csi20/Data/Stanford"
        DataPath="/media/cs1623/One Touch/Backup_April2023/Dropbox/phd/Projects/Stanford/Data/DICOM_Gated_CT"

        filepath=f'{DataPath}/{case}/MT/SW-0.0-BE-1e-9'
        final_ind_def_path=f"{filepath}/area_global_final_ind.txt"
        final_ind_vol_path=f"{filepath}/area_global_vol_final_ind.txt"

    elif case[0]=='P':
        print("Portugal cohort")

        final_ind_def_path=f"{home_dir}/Data/portugal/{case}/MT/SW-0.0-BE-1e-9/area_global_final_ind.txt"
        final_ind_vol_path=f"{home_dir}/Data/portugal/{case}/MT/SW-0.0-BE-1e-9/area_global_vol_final_ind.txt"
    
    elif case[0]=='V':
        print("Vitaliy cohort")
    
        final_ind_def_path=f"{home_dir}/Data/Vitaliy/{case}/LA/MT-20f/SW-0.0-BE-1e-9/area_global_final_ind.txt"
        final_ind_vol_path=f"{home_dir}/Data/Vitaliy/{case}/LA/MT-20f/SW-0.0-BE-1e-9/area_global_vol_final_ind.txt"

        final_ind_def_path=f"/media/cs1623/Elements/Vitaliy/{case}/LA/MT-20f/SW-0.0-BE-1e-9/area_global_final_ind.txt"
        final_ind_vol_path=f"/media/cs1623/Elements/Vitaliy/{case}/LA/MT-20f/SW-0.0-BE-1e-9/area_global_vol_final_ind.txt"

        final_ind_def_path=f"/media/cs1623/Elements/Vitaliy_BiV/{case}/LA/MT-20f/SW-0.0-BE-1e-9/area_global_final_ind.txt"
        final_ind_vol_path=f"/media/cs1623/Elements/Vitaliy_BiV/{case}/LA/MT-20f/SW-0.0-BE-1e-9/area_global_vol_final_ind.txt"

    if os.path.isfile(final_ind_def_path):
        print("File using default path exists")
        
        final_ind=np.loadtxt(final_ind_def_path)
        final_ind=int(final_ind)
        
        print("final ind", final_ind, "\n")

    elif os.path.isfile(final_ind_vol_path):
        print("File using vol path exists")
        
        final_ind=np.loadtxt(final_ind_vol_path)
        final_ind=final_ind/2.0
        final_ind=int(final_ind)
        
        print("final ind", final_ind, "\n")
    
    else:
        print("Neither file exists\n")
        final_ind=np.nan

    return final_ind

def retrieve_final_ind_long(case, laptop=False):

    """
    Get index of point where notch is using long global strain transient.
    """

    if laptop:
        print("On bioeng347-lap!")
        home_dir="/home/csi20local"
    else:
        print("Not on laptop!")
        home_dir="/home/csi20"
    
    if case[0]=='V':
        print("Vitaliy cohort")
    
        final_ind_def_path=f"{DataPath}/{case}/LA/MT/SW-0.0-BE-1e-9/long_global_final_ind.txt"
        final_ind_vol_path=f"{DataPath}/{case}/LA/MT/SW-0.0-BE-1e-9/long_global_vol_final_ind.txt"

        # final_ind_def_path=f"/media/cs1623/Elements/Vitaliy/{case}/LA/MT/SW-0.0-BE-1e-9/long_global_final_ind.txt"
        # final_ind_vol_path=f"/media/cs1623/Elements/Vitaliy/{case}/LA/MT/SW-0.0-BE-1e-9/long_global_vol_final_ind.txt"

    if os.path.isfile(final_ind_def_path):
        print("File using default path exists")
        
        print(final_ind_def_path)
        final_ind=np.loadtxt(final_ind_def_path)
        final_ind=int(final_ind)
        
        print("final ind", final_ind, "\n")

    elif os.path.isfile(final_ind_vol_path):
        print("File using vol path exists")
        
        final_ind=np.loadtxt(final_ind_vol_path)
        final_ind=final_ind/2.0
        final_ind=int(final_ind)
        
        print("final ind", final_ind, "\n")
    
    else:
        print("Neither file exists\n")
        final_ind=np.nan

    return final_ind

def retrieve_final_ind_20f_long(case, laptop=False):

    """
    Get index of point where notch is. Firstly tries notch from global strain transient, and then global volume transient.
    """

    if laptop:
        print("On bioeng347-lap!")
        home_dir="/home/csi20local"
    else:
        print("Not on laptop!")
        home_dir="/home/csi20"

    if ((case[0] == "E") or (case[0] == "C")):
        print("GSTT cohort")
        DataPath="/home/csi20/Dropbox/phd/Data/RG_CT_Cases"
        if case in f20_cases:
            filepath=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9'
        
        else:
            filepath=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9'
    
    elif case[0]=='S':
        print("Stanford cohort")
        DataPath="/home/csi20/Data/Stanford"
        DataPath="/media/cs1623/One Touch/Backup_April2023/Dropbox/phd/Projects/Stanford/Data/DICOM_Gated_CT"

        filepath=f'{DataPath}/{case}/MT/SW-0.0-BE-1e-9'
        final_ind_def_path=f"{filepath}/area_global_final_ind.txt"
        final_ind_vol_path=f"{filepath}/area_global_vol_final_ind.txt"

    elif case[0]=='P':
        print("Portugal cohort")

        final_ind_def_path=f"{home_dir}/Data/portugal/{case}/MT/SW-0.0-BE-1e-9/area_global_final_ind.txt"
        final_ind_vol_path=f"{home_dir}/Data/portugal/{case}/MT/SW-0.0-BE-1e-9/area_global_vol_final_ind.txt"
    
    elif case[0]=='V':
        print("Vitaliy cohort")

        final_ind_def_path=f"/media/cs1623/Elements/Vitaliy_BiV/{case}/LA/MT-20f/SW-0.0-BE-1e-9/long_global_final_ind.txt"
        final_ind_vol_path=f"/media/cs1623/Elements/Vitaliy_BiV/{case}/LA/MT-20f/SW-0.0-BE-1e-9/long_global_vol_final_ind.txt"

    if os.path.isfile(final_ind_def_path):
        print("File using default path exists")
        
        final_ind=np.loadtxt(final_ind_def_path)
        final_ind=int(final_ind)
        
        print("final ind", final_ind, "\n")

    elif os.path.isfile(final_ind_vol_path):
        print("File using vol path exists")
        
        final_ind=np.loadtxt(final_ind_vol_path)
        final_ind=final_ind/2.0
        final_ind=int(final_ind)
        
        print("final ind", final_ind, "\n")
    
    else:
        print("Neither file exists\n")
        final_ind=np.nan

    return final_ind

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
    
    if ((case[0] == "E") or (case[0] == "C")):
        print("GSTT cohort")
        DataPath="/home/csi20/Dropbox/phd/Data/RG_CT_Cases"
        if case in f20_cases:
            filepath=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9'
        
        else:
            filepath=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9'

        data = np.loadtxt(f'{filepath}/{strain_type}_meanstrains_{region}_excl_PVs.txt')
    
    elif case[0]=='S':
        print("Stanford cohort")
        DataPath="/home/csi20/Dropbox/phd/Projects/Stanford/Data/DICOM_Gated_CT"
        DataPath="/home/csi20/Data/Stanford"
        DataPath="/media/cs1623/One Touch/Backup_April2023/Dropbox/phd/Projects/Stanford/Data/DICOM_Gated_CT"

        filepath=f'{DataPath}/{case}/MT/SW-0.0-BE-1e-9'
        # filepath=f'{DataPath}/{case}/MT-20f/SW-0.0-BE-1e-9'

        data = np.loadtxt(f'{filepath}/{strain_type}_meanstrains_{region}_excl_PVs_mshqual.txt')

    elif case[0]=='P':
        print("Portugal cohort")
        DataPath="/home/csi20/Data/portugal"
        DataPath="/media/csi20local/Elements/portugal"

        filepath=f'{DataPath}/{case}/MT/SW-0.0-BE-1e-9'
        data = np.loadtxt(f'{filepath}/{strain_type}_meanstrains_{region}_excl_PVs_mshqual.txt')

    elif case[0]=='V':
        print("Vitaliy cohort")
        filepath=f"/home/csi20/Data/Vitaliy/{case}/LA/MT/SW-0.0-BE-1e-9"
        # filepath=f"/media/cs1623/Elements/Vitaliy/{case}/LA/MT/SW-0.0-BE-1e-9"
        # filepath=f"/media/cs1623/Elements1/Vitaliy_BiV/{case}/LA/MT/SW-0.0-BE-1e-9"

        data = np.loadtxt(f'{filepath}/{strain_type}_meanstrains_{region}_excl_PVs_mshqual.txt')
            
    return data

def retrieve_area_strain_transient_20f(case, strain_type, region):
    """
    Use this function to retrieve global and regional area/squeez strain transients.
    Previously called retrieve_area_data.

    Transients exclude LAA and PVs strains.

    Usage:
        * case: case
        * strain_type: 'area' or 'squeez'
        * region: 'global', 'roof', 'lat', 'sept', 'ant', 'post'
    """
    
    if case[0]=='V':
        print("Vitaliy cohort")
        filepath=f"/media/cs1623/Elements/Vitaliy/{case}/LA/MT-20f/SW-0.0-BE-1e-9"
        data = np.loadtxt(f'{filepath}/{strain_type}_meanstrains_{region}_excl_PVs_mshqual.txt')
            
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
    
    # if case in f20_cases:
    #     # filepath=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9'
    #     filepath=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9/percent_regional_strains'
    
    # else:
    #     # filepath=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9'
    #     filepath=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9/percent_regional_strains'

    filepath=f'{DataPath}/{case}/LA/MT/SW-0.0-BE-1e-9'
        
    data = np.loadtxt(f'{filepath}/{fibre_arch}_excl_PVs_mshqual_meanstrains_{region}.txt')[component]
    
    return data

def retrieve_Long_Circ_strain_transient(case, region):
    """
    Use this function to retrieve global and regional longitudinal and circumferential strain transients.

    Usage:
        * region: global, ant, lat, post, roof, sept

    Returns:
        * lng_strains, crc_strains
    """

    filepath=f'{DataPath}/{case}/LA/MT/SW-0.0-BE-1e-9'

    if region=="global":
        
        data = np.loadtxt(f'{filepath}/lng_crc_excl_PVs_mshqual_meanstrains_{region}.txt')

    else:

        data = np.loadtxt(f'{filepath}/lng_circ_excl_PVs_mshqual_meanstrains_{region}.txt')
    
    lng_strains = data[0, :]
    crc_strains = data[1, :]

    return lng_strains, crc_strains

def retrieve_Long_Circ_strain_transient_20f(case, region):
    """
    Use this function to retrieve global and regional longitudinal and circumferential strain transients.

    Usage:
        * region: global, ant, lat, post, roof, sept

    Returns:
        * lng_strains, crc_strains
    """

    filepath=f'{DataPath}/{case}/LA/MT-20f/SW-0.0-BE-1e-9'

    if region=="global":
        
        data = np.loadtxt(f'{filepath}/lng_crc_excl_PVs_mshqual_meanstrains_{region}.txt')

    else:

        data = np.loadtxt(f'{filepath}/lng_circ_excl_PVs_mshqual_meanstrains_{region}.txt')
    
    lng_strains = data[0, :]
    crc_strains = data[1, :]

    return lng_strains, crc_strains

def retrieve_2d_long_transient(case, view):
    """
    Use this function to retrieve 2d global longitudinal strain transient.

    Usage:
        * view: '4chamber' or '2chamber'

    Returns:
        * lng_strains
    """

    filepath=f'{DataPath}/{case}/LA/MT/SW-0.0-BE-1e-9'

    data = np.loadtxt(f'{filepath}/{view}_strain_transient.txt')
    
    lng_strains = data
    print(lng_strains.shape)
    
    return lng_strains

def retrieve_2d_long_transient_20f(case, view, va_method=False):
    """
    Use this function to retrieve 2d global longitudinal strain transient.

    Usage:
        * view: '4chamber' or '2chamber'

    Returns:
        * lng_strains
    """

    filepath=f'{DataPath}/{case}/LA/MT-20f/SW-0.0-BE-1e-9'

    if va_method:
        print("Retrieving VA method strains")
        path=f'{filepath}/{view}_va_strain_transient.txt'
        print(path)
        data = np.loadtxt(path)

    else:
        print("Retrieving automatic method strains")
        path=f'{filepath}/{view}_strain_transient.txt'
        print(path)
        data = np.loadtxt(path)
    
    lng_strains = data
    print(lng_strains.shape)
    
    return lng_strains

def retrieve_area_strain_transient_Vxm(case, strain_type, region):
    """
    Use this function to retrieve global and regional area/squeez strain transients from Vxm FT.
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


def get_tsffd_trackingpath(case):
    """
    Use this function to get TSFFD tracking path

    Usage:
        * case: case
    """
    
    if ((case[0] == "E") or (case[0] == "C")):
        print("GSTT cohort")
        DataPath="/home/csi20/Dropbox/phd/Data/RG_CT_Cases"
        if case in f20_cases:
            filepath=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9'
        
        else:
            filepath=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9'

    elif case[0]=='S':
        print("Stanford cohort")
        DataPath="/home/csi20/Dropbox/phd/Projects/Stanford/Data/DICOM_Gated_CT"
        DataPath="/home/csi20/Data/Stanford"
        DataPath=f"/media/cs1623/One Touch/Backup_April2023/Dropbox/phd/Projects/Stanford/Data/DICOM_Gated_CT"

        filepath=f'{DataPath}/{case}/MT/SW-0.0-BE-1e-9'  
        # filepath=f'{DataPath}/{case}/MT-20f/SW-0.0-BE-1e-9'  

    elif case[0]=='P':
        print("Portugal cohort")
        DataPath="/home/csi20/Data/portugal"
        # DataPath="/media/csi20local/One Touch/Backup_April2023/Dropbox/phd/Projects/Stanford/Data/DICOM_Gated_CT"

        filepath=f'{DataPath}/{case}/MT/SW-0.0-BE-1e-9'

    elif case[0]=='V':
        print("Vitaliy cohort")
        DataPath="/home/csi20/Data/Vitaliy"
        # DataPath="/media/csi20local/One Touch/Backup_April2023/Dropbox/phd/Projects/Stanford/Data/DICOM_Gated_CT"
        # DataPath="/media/cs1623/Elements/Vitaliy"
        # DataPath="/media/cs1623/Elements1/Vitaliy_BiV"

        filepath=f'{DataPath}/{case}/LA/MT/SW-0.0-BE-1e-9'       
    
    return filepath

def get_tsffd_trackingpath_20f(case):
    """
    Use this function to get TSFFD tracking path

    Usage:
        * case: case
    """
    
    if case[0]=='V':
        print("Vitaliy cohort")
        filepath=f'{DataPath}/{case}/LA/MT-20f/SW-0.0-BE-1e-9' 

    else:
        print("Error in get_tsffd_trackingpath_20f!")
    
    return filepath

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

def write_pts(pts,filename):

        print('Writing '+filename+'...')

        assert pts.shape[1] == 3
        with open(filename, 'w') as fp:
                fp.write('{}\n'.format(pts.shape[0]))
                for pnt in pts:
                        fp.write('{0[0]} {0[1]} {0[2]}\n'.format(pnt))
        fp.close()

def write_elem(elem,
                           tags,
                           filename,
                           el_type='Tt'):
        print('Writing '+filename+'...')

        if el_type=='Tt':
                assert elem.shape[1] == 4
        elif el_type=='Tr':
                assert elem.shape[1] == 3
        elif el_type=='Ln':
                assert elem.shape[1] == 2
        else:
                raise Exception('element type not recognised. Accepted: Tt, Tr, Ln')

        assert elem.shape[0] == tags.shape[0]

        with open(filename, 'w') as fe:
                fe.write('{}\n'.format(elem.shape[0]))
                for i,el in enumerate(elem):
                        fe.write(el_type)
                        for e in el:
                                fe.write(' '+str(e))
                        fe.write(' '+str(tags[i]))
                        fe.write('\n')
        fe.close()