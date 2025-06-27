import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

"""
GLOBAL errors for given (SW, BE) across cases.

Inputs: Error type, Baseline SW1 (string) BE1 (float) for MT FIMH cases, SW2 BE2 for Opt 30 cases.

UPDATED 25 OCT: 30 cases
"""


def Plot_GlobalError_AcrossCases_axis_30Cases(Error, SW_Pop1, BE_Pop1, SW_Pop2, BE_Pop2, ax):

    data_Baseline = []
    data_New_List = []
    
    FIMH_CaseList = ['01', '02', '05', '06', '07', '08', '09', '12', '15', '16']
    FIMH_CaseList = ['CT-CRT-' + case for case in FIMH_CaseList]
    
    New_CaseList = ['01', '02', '05', '06', '07', '08', '09', '10', '12', '14', '15', '16',
                    '17', '18', '19', '20', '21', '23', '24', '25', '26', '27', '28', '29',
                    '30', '32']
    New_CaseList = ['CT-CRT-' + case for case in New_CaseList]
    New_Cases = ['EBR-01', 'EBR-02', 'Normal-1', 'Normal-3']
    New_CaseList = New_CaseList + New_Cases
    
    # TDownsampled case list
    TDownsampled_Cases = ['21', '23', '24', '25', '26', '27', '28', '29',
                    '30', '32']
    TDownsampled_Cases = ['CT-CRT-' + case for case in TDownsampled_Cases]
    TDownsampled_Cases.append('EBR-01')
    TDownsampled_Cases.append('EBR-02')

    for Case in New_CaseList:
        
        if Error == 'ASD':
            csv_name = 'Normal-Distance-Results'

        elif Error == 'DHD':
            csv_name = 'Hausdorff-Distance-Results'

        elif Error == 'DSC':
            csv_name = 'Dice-Results'
            
        else:
            print("Error should be one of: ASD, DHD. DSC.")
            
        if Case in TDownsampled_Cases:
            df = pd.read_csv(f'/home/csi20/Dropbox/phd/Data/RG_CT_Cases/{Case}/csv_results/MT-HiRes-TDownsampled-{csv_name}.csv', 
                        sep = ' ', index_col = 0)
            data_New_List.append(df.loc[BE_Pop2].loc[f'{SW_Pop2}'])

            df_base = pd.read_csv(f'/home/csi20/Dropbox/phd/Data/RG_CT_Cases/{Case}/csv_results/MT-TDownsampled-{csv_name}.csv', 
                        sep = ' ', index_col = 0)
            data_Baseline.append(df_base.loc[BE_Pop1].loc[f'{SW_Pop1}'])

        else:
            df = pd.read_csv(f'/home/csi20/Dropbox/phd/Data/RG_CT_Cases/{Case}/csv_results/MT-HiRes-{csv_name}.csv', 
                        sep = ' ', index_col = 0)
            data_New_List.append(df.loc[BE_Pop2].loc[f'{SW_Pop2}'])

            df_base = pd.read_csv(f'/home/csi20/Dropbox/phd/Data/RG_CT_Cases/{Case}/csv_results/MT-{csv_name}.csv', 
                        sep = ' ', index_col = 0)
            data_Baseline.append(df_base.loc[BE_Pop1].loc[f'{SW_Pop1}'])
            

    ErrorUnits = {
          "ASD": "[mm]",
          "DHD": "[mm]",
          "DSC": ""
        }

    units = ErrorUnits[f'{Error}']

    c = 'red'
    c2 = 'blue'
    
    ax.boxplot(data_Baseline, labels=['Base. TSFFD 30 Cases'], positions=[0], medianprops=dict(color=c), boxprops=dict(color=c))
    ax.boxplot(data_New_List, labels=['Opt. TSFFD 30 Cases'], positions=[1], medianprops=dict(color=c2), boxprops=dict(color=c2))
    
    ax.set_ylabel(f'{Error} {units}', fontsize=17)

"""
GLOBAL errors for given (SW, BE) across cases.

Inputs: Error type, BE (float) and SW (string) for MT & FIMH cases, BE and SW for 30 cases.

UPDATED 25 OCT: 30 cases

Use this function to perform a ttest on original and optimised TSFFD configurations
"""

# def GlobalError_30Cases_ttest(Error, SW_Pop1, BE_Pop1, SW_Pop2, BE_Pop2):

#     data_Baseline = []
#     data_New_List = []
    
#     # OG_CaseList = ['01', '02', '05', '06', '07', '08', '09', '12', '15', '16']
#     # OG_CaseList = ['CT-CRT-' + case for case in OG_CaseList]
#     New_CaseList = ['01', '02', '05', '06', '07', '08', '09', '10', '12', '14', '15', '16',
#                     '17', '18', '19', '20', '21', '23', '24', '25', '26', '27', '28', '29',
#                     '30', '32']
#     New_CaseList = ['CT-CRT-' + case for case in New_CaseList]
#     New_Cases = ['EBR-01', 'EBR-02', 'Normal-1', 'Normal-3']
#     New_CaseList = New_CaseList + New_Cases
    
#     TDownsampled_Cases = ['21', '23', '24', '25', '26', '27', '28', '29',
#                     '30', '32']
#     TDownsampled_Cases = ['CT-CRT-' + case for case in TDownsampled_Cases]
#     TDownsampled_Cases.append('EBR-01')
#     TDownsampled_Cases.append('EBR-02')

#     for Case in New_CaseList:
        
#         if Error == 'ASD':
#             csv_name = 'Normal-Distance-Results'

#         elif Error == 'DHD':
#             csv_name = 'Hausdorff-Distance-Results'

#         elif Error == 'DSC':
#             csv_name = 'Dice-Results'
            
#         else:
#             print("Error should be one of: ASD, DHD. DSC.")
            
#         if Case in TDownsampled_Cases:
#             df = pd.read_csv(f'/home/csi20local/Data/RG_CT_Cases/{Case}/MT-HiRes-TDownsampled-{csv_name}.csv', 
#                         sep = ' ', index_col = 0)
#             data_New_List.append(df.loc[BE_Pop2].loc[f'{SW_Pop2}'])

#             df_base = pd.read_csv(f'/home/csi20local/Data/RG_CT_Cases/{Case}/MT-TDownsampled-{csv_name}.csv', 
#                         sep = ' ', index_col = 0)

#             data_Baseline.append(df_base.loc[BE_Pop1].loc[f'{SW_Pop1}'])
            
#         else:
#             df = pd.read_csv(f'/home/csi20local/Data/RG_CT_Cases/{Case}/MT-HiRes-{csv_name}.csv', 
#                         sep = ' ', index_col = 0)
#             data_New_List.append(df.loc[BE_Pop2].loc[f'{SW_Pop2}'])

#             df_base = pd.read_csv(f'/home/csi20local/Data/RG_CT_Cases/{Case}/MT-{csv_name}.csv', 
#                         sep = ' ', index_col = 0)

#             data_Baseline.append(df_base.loc[BE_Pop1].loc[f'{SW_Pop1}'])

#     return ttest_ind(data_Baseline, data_New_List, equal_var=False)

def GlobalError_30Cases_ttest(Error, SW_Pop1, BE_Pop1, SW_Pop2, BE_Pop2):

    data_Baseline = []
    data_New_List = []
    
    New_CaseList = ['01', '02', '05', '06', '07', '08', '09', '10', '12', '14', '15', '16',
                    '17', '18', '19', '20', '21', '23', '24', '25', '26', '27', '28', '29',
                    '30', '32']
    New_CaseList = ['CT-CRT-' + case for case in New_CaseList]
    New_Cases = ['EBR-01', 'EBR-02', 'Normal-1', 'Normal-3']
    New_CaseList = New_CaseList + New_Cases
    
    TDownsampled_Cases = ['21', '23', '24', '25', '26', '27', '28', '29',
                    '30', '32']
    TDownsampled_Cases = ['CT-CRT-' + case for case in TDownsampled_Cases]
    TDownsampled_Cases.append('EBR-01')
    TDownsampled_Cases.append('EBR-02')

    error_dict = {'ASD': 'Normal-Distance-Results', 'DHD': 'Hausdorff-Distance-Results', 'DSC': 'Dice-Results',
                 'LAA': 'LAA-AbsoluteError', 'LSPV': 'LSPV-AbsoluteError', 'LIPV': 'LIPV-AbsoluteError',
                 'RSPV': 'RSPV-AbsoluteError', 'RIPV': 'RIPV-AbsoluteError',
                 'LAA-LS': 'LAA-LS-PercentageErrors', 'LAA-LI': 'LAA-LI-PercentageErrors', 
                 'LAA-RS': 'LAA-RS-PercentageErrors', 'LAA-RI': 'LAA-RS-PercentageErrors',
                 'LS-LI': 'LS-LI-PercentageErrors', 'LS-RS': 'LS-RS-PercentageErrors', 
                 'LS-RI': 'LS-RI-PercentageErrors', 'LI-RS': 'LI-RS-PercentageErrors', 
                 'LI-RI': 'LI-RI-PercentageErrors', 'RS-RI': 'RS-RI-PercentageErrors',
                 'MV': 'MV-AbsoluteError'}

    csv_name = error_dict[Error]

    for Case in New_CaseList:
        
        # Remove C9 if Error involves LAA
        if 'LAA' in Error:

            if 'CT-CRT-09' in New_CaseList:
                New_CaseList = list(New_CaseList)
                New_CaseList.remove('CT-CRT-09')
                New_CaseList = tuple(New_CaseList)
            
        # Remove C18, C23, N3 if Error involves LIPV
        if 'LI' in Error:
            
            if 'CT-CRT-18' in New_CaseList:
                New_CaseList = list(New_CaseList)
                New_CaseList.remove('CT-CRT-18')
                New_CaseList = tuple(New_CaseList)

            if 'CT-CRT-23' in New_CaseList:
                New_CaseList = list(New_CaseList)
                New_CaseList.remove('CT-CRT-23')
                New_CaseList = tuple(New_CaseList)

            if 'Normal-3' in New_CaseList:
                New_CaseList = list(New_CaseList)
                New_CaseList.remove('Normal-3')
                New_CaseList = tuple(New_CaseList)
            
    for Case in New_CaseList:
            
        if Case in TDownsampled_Cases:
            df = pd.read_csv(f'/home/csi20/Dropbox/phd/Data/RG_CT_Cases/{Case}/csv_results/MT-HiRes-TDownsampled-{csv_name}.csv', 
                        sep = ' ', index_col = 0)
            data_New_List.append(df.loc[BE_Pop2].loc[f'{SW_Pop2}'])

            df_base = pd.read_csv(f'/home/csi20/Dropbox/phd/Data/RG_CT_Cases/{Case}/csv_results/MT-TDownsampled-{csv_name}.csv', 
                        sep = ' ', index_col = 0)

            data_Baseline.append(df_base.loc[BE_Pop1].loc[f'{SW_Pop1}'])
            
        else:
            df = pd.read_csv(f'/home/csi20/Dropbox/phd/Data/RG_CT_Cases/{Case}/csv_results/MT-HiRes-{csv_name}.csv', 
                        sep = ' ', index_col = 0)
            data_New_List.append(df.loc[BE_Pop2].loc[f'{SW_Pop2}'])

            df_base = pd.read_csv(f'/home/csi20/Dropbox/phd/Data/RG_CT_Cases/{Case}/csv_results/MT-{csv_name}.csv', 
                        sep = ' ', index_col = 0)

            data_Baseline.append(df_base.loc[BE_Pop1].loc[f'{SW_Pop1}'])

    return ttest_ind(data_Baseline, data_New_List, equal_var=False)

"""
Retrieves data in the form of a list.

INPUT: Error type, Resolution, SW, BE
"""

# def Retrieve_data(Error, Res, SW, BE):

#     data = []
    
#     New_CaseList = ['01', '02', '05', '06', '07', '08', '09', '10', '12', '14', '15', '16',
#                     '17', '18', '19', '20', '21', '23', '24', '25', '26', '27', '28', '29',
#                     '30', '32']
#     New_CaseList = ['CT-CRT-' + case for case in New_CaseList]
#     New_Cases = ['EBR-01', 'EBR-02', 'Normal-1', 'Normal-3']
#     New_CaseList = New_CaseList + New_Cases
    
#     # TDownsampled case list
#     TDownsampled_Cases = ['21', '23', '24', '25', '26', '27', '28', '29',
#                     '30', '32']
#     TDownsampled_Cases = ['CT-CRT-' + case for case in TDownsampled_Cases]
#     TDownsampled_Cases.append('EBR-01')
#     TDownsampled_Cases.append('EBR-02')

#     for Case in New_CaseList:
        
#         if Error == 'ASD':
#             csv_name = 'Normal-Distance-Results'

#         elif Error == 'DHD':
#             csv_name = 'Hausdorff-Distance-Results'

#         elif Error == 'DSC':
#             csv_name = 'Dice-Results'
            
#         else:
#             print("Error should be one of: ASD, DHD. DSC.")
            
#         if Case in TDownsampled_Cases:
#             df = pd.read_csv(f'/home/csi20local/Data/RG_CT_Cases/{Case}/{Res}-TDownsampled-{csv_name}.csv', 
#                         sep = ' ', index_col = 0)
#             data.append(df.loc[BE].loc[f'{SW}'])

#         else:
#             df = pd.read_csv(f'/home/csi20local/Data/RG_CT_Cases/{Case}/{Res}-{csv_name}.csv', 
#                         sep = ' ', index_col = 0)
#             data.append(df.loc[BE].loc[f'{SW}'])

#     return data

def Retrieve_data(Error, Res, SW, BE):

    data = []
    
    # Full 30 case list
    New_CaseList = ['01', '02', '05', '06', '07', '08', '09', '10', '12', '14', '15', '16',
                    '17', '18', '19', '20', '21', '23', '24', '25', '26', '27', '28', '29',
                    '30', '32']
    New_CaseList = ['CT-CRT-' + case for case in New_CaseList]
    New_Cases = ['EBR-01', 'EBR-02', 'Normal-1', 'Normal-3']
    New_CaseList = New_CaseList + New_Cases
    
    # TDownsampled case list
    TDownsampled_Cases = ['21', '23', '24', '25', '26', '27', '28', '29',
                    '30', '32']
    TDownsampled_Cases = ['CT-CRT-' + case for case in TDownsampled_Cases]
    TDownsampled_Cases.append('EBR-01')
    TDownsampled_Cases.append('EBR-02')

    error_dict = {'ASD': 'Normal-Distance-Results', 'DHD': 'Hausdorff-Distance-Results', 'DSC': 'Dice-Results',
                 'LAA': 'LAA-AbsoluteError', 'LSPV': 'LSPV-AbsoluteError', 'LIPV': 'LIPV-AbsoluteError',
                 'RSPV': 'RSPV-AbsoluteError', 'RIPV': 'RIPV-AbsoluteError',
                 'LAA-LS': 'LAA-LS-PercentageErrors', 'LAA-LI': 'LAA-LI-PercentageErrors', 
                 'LAA-RS': 'LAA-RS-PercentageErrors', 'LAA-RI': 'LAA-RS-PercentageErrors',
                 'LS-LI': 'LS-LI-PercentageErrors', 'LS-RS': 'LS-RS-PercentageErrors', 
                 'LS-RI': 'LS-RI-PercentageErrors', 'LI-RS': 'LI-RS-PercentageErrors', 
                 'LI-RI': 'LI-RI-PercentageErrors', 'RS-RI': 'RS-RI-PercentageErrors',
                 'MV': 'MV-AbsoluteError'}

    csv_name = error_dict[Error]

    for Case in New_CaseList:

        # Remove C9 if Error involves LAA
        if 'LAA' in Error:

            if 'CT-CRT-09' in New_CaseList:
                New_CaseList = list(New_CaseList)
                New_CaseList.remove('CT-CRT-09')
                New_CaseList = tuple(New_CaseList)
            
        # Remove C18, C23, N3 if Error involves LIPV
        if 'LI' in Error:
            
            if 'CT-CRT-18' in New_CaseList:
                New_CaseList = list(New_CaseList)
                New_CaseList.remove('CT-CRT-18')
                New_CaseList = tuple(New_CaseList)

            if 'CT-CRT-23' in New_CaseList:
                New_CaseList = list(New_CaseList)
                New_CaseList.remove('CT-CRT-23')
                New_CaseList = tuple(New_CaseList)

            if 'Normal-3' in New_CaseList:
                New_CaseList = list(New_CaseList)
                New_CaseList.remove('Normal-3')
                New_CaseList = tuple(New_CaseList)
        
    for Case in New_CaseList:

        if Case in TDownsampled_Cases:
            df = pd.read_csv(f'/home/csi20/Dropbox/phd/Data/RG_CT_Cases/{Case}/csv_results/{Res}-TDownsampled-{csv_name}.csv', 
                        sep = ' ', index_col = 0)
            data.append(df.loc[BE].loc[f'{SW}'])

        else:
            df = pd.read_csv(f'/home/csi20/Dropbox/phd/Data/RG_CT_Cases/{Case}/csv_results/{Res}-{csv_name}.csv', 
                        sep = ' ', index_col = 0)
            data.append(df.loc[BE].loc[f'{SW}'])

    return data