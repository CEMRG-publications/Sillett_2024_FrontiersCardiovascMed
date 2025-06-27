import numpy as np

numTimes = 10

nTime=np.arange(0, numTimes)/numTimes

DataPath="/home/csi20local/Dropbox/phd/Data/RG_CT_Cases"

f20_cases = ['21', '23', '24', '26', '28', '29', '31']
f20_cases = [f'CT-CRT-{case_ind}' for case_ind in f20_cases]

def plot_strain(ax, case, label, strain_type):
    
    if case in f20_cases:
        filepath=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9'
    
    else:
        filepath=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9'
        
    if strain_type[0] == 'e': ## fibre strain
        data = np.loadtxt(f'{filepath}/{strain_type}_meanstrains_global.txt')
        
        print("This branch is a WIP LOL")
#         ax.plot(nTime, data[0], label=label)
#         ax.plot(nTime, data[1], ls='--')   
    
    else: ## area or squeez
        data = np.loadtxt(f'{filepath}/{strain_type}_meanstrains_global.txt')
        ax.plot(nTime, data, label=label)

def data_range(case, strain_type, region):
    """
    Use this function to retrieve range of area meanstrains_{region} transients
    Usage for strain_type:
        * area 
        * squeez
    Usage for region:
        * global
        * ant
        * lat
        * post
        * roof
        * sept
    """
    
    if case in f20_cases:
        filepath=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9'
    
    else:
        filepath=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9'
        
    data = np.loadtxt(f'{filepath}/{strain_type}_meanstrains_{region}.txt')
    data_range = np.ptp(data)
    
    return data_range

def retrieve_fibres_data(case, strain_type, component):
    """
    Use this function to retrieve global fibre meanstrains transients
    Usage for strain_type:
        * endo_avg
        * epi_avg
    """
    
    if case in f20_cases:
        filepath=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9'
    
    else:
        filepath=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9'
        
    data = np.loadtxt(f'{filepath}/{strain_type}_meanstrains_global.txt')[component]
#     data_range = np.ptp(data)
    
    return data

def data_range_fibres(case, strain_type, component):
    """
    Use this function to retrieve range of global meanstrains transients for fibre strains
    Usage for strain_type:
        * endo_avg
        * epi_avg
    """
    
    if case in f20_cases:
        filepath=f'{DataPath}/{case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9'
    
    else:
        filepath=f'{DataPath}/{case}/MT-HiRes/SW-0.0-BE-1e-9'
        
    data = np.loadtxt(f'{filepath}/{strain_type}_meanstrains_global.txt')[component]
    data_range = np.ptp(data)
    
    return data_range