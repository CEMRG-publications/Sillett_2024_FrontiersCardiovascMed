import numpy as np
import pandas as pd

# Create list of cases with 20 time frames
TDownsampledCases = ['21', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '34']
TDownsampledCases = ['CT-CRT/case' + case for case in TDownsampledCases]
TDownsampledCases_add = ['EBR/case01', 'EBR/case02']
TDownsampledCases = TDownsampledCases + TDownsampledCases_add

def S_unified(case_list, Error):
    """
    Calculates unified z-score of all (SW,BE) combo's across a provided list of cases for training. 

    INPUT: List of cases. Error type.

    OUTPUT: Mean, std deviation, DataFrame of medians (across cases) of each hyperparameter combination, DataFrame of
            z score of each hyperparameter combination across cases
    """
    
    # Dict to convert error nickname to csv filename
    error_dict = {'ASD': 'Normal-Distance-Results', 'DHD': 'Hausdorff-Distance-Results', 'Dice': 'Dice-Results'}
    
    Error = error_dict[Error]
    
    # Create array to hold errors across cases for each (SW,BE) participant
    cases_array = np.zeros(shape=(63,len(case_list)))
        
    for Case in case_list:
        
        if Case in TDownsampledCases:
            df_read = pd.read_csv(f'/home/csi20/Dropbox/phd/Data/RG_CT_Cases/{Case}/csv_results/MT-HiRes-TDownsampled-{Error}.csv', 
                        sep = ' ', index_col = 0)
            df_array = df_read.to_numpy() 
            flattened_array = np.reshape(df_array, 63) # flatten array to 1D array with 63 elements
    
            cases_array[:, case_list.index(Case)] = flattened_array # assign flattened array to corresponding case col.
    
        else:
            df_read = pd.read_csv(f'/home/csi20/Dropbox/phd/Data/RG_CT_Cases/{Case}/csv_results/MT-HiRes-{Error}.csv', 
                        sep = ' ', index_col = 0)
            df_array = df_read.to_numpy()
            flattened_array = np.reshape(df_array, 63)
                
            cases_array[:, case_list.index(Case)] = flattened_array
                
    # Create array for medians of errors for each (SE, BE) combo across cases
    medians = np.zeros(63)

    for i in range(0,cases_array.shape[0]):
        # Take median across case columns for each (SW,BE) participant and assign to medians array
        medians[i] = np.median(cases_array[i, :])
            
    # Find mean and std dev of medians across 63 (SW, BE) combinations
    mean = np.mean(medians)
    std = np.std(medians)
        
    BE_rename = {0: 4e-6, 1: 1e-6, 2: 4e-7, 3: 1e-7, 4: 4e-8, 5: 1e-8, 6: 4e-9, 7: 1e-9, 8: 4e-10}
    SW_rename = {0: '9e-2', 1: '3e-2', 2: '9e-3', 3: '3e-3', 4: '9e-4', 5: '3e-4', 6: '0.0'}
  
    # Create Dataframe of Median error for each (SW, BE) combination 
    df_medians = np.reshape(medians, (9,7))
    df_medians = pd.DataFrame(df_medians)
    df_medians = df_medians.rename(index = BE_rename, columns=SW_rename)
    
    # Create Dataframe of Z scores for each (SE, BE) combination
    df_zscore = (df_medians-mean)/std
    df_zscore = df_zscore.rename(index = BE_rename, columns=SW_rename)
    
    if Error == "Dice-Results":
        
        # Correct mean and medians in the case of minimising DSC means improving segmentation
        mean = 1 - mean
        df_medians = 1 - df_medians
        
        df_zscore = (df_medians-mean)/std
#         df_zscore = 1 - df_zscore # Old code
    
    return mean, std, df_medians, df_zscore

def S_unified_local(case_list, Error):
    """
    Calculates unified z-score of all (SW,BE) combo's across a provided list of cases for training. 

    INPUT: List of cases. Error type.

    OUTPUT: Mean, std deviation, DataFrame of medians (across cases) of each hyperparameter combination, DataFrame of
            z score of each hyperparameter combination across cases
    """
    
    # Dict to convert error nickname to csv filename
    error_dict = {'ASD': 'Normal-Distance-Results', 'DHD': 'Hausdorff-Distance-Results', 'Dice': 'Dice-Results'}
    
    Error = error_dict[Error]
    
    # Create array to hold errors across cases for each (SW,BE) participant
    cases_array = np.zeros(shape=(63,len(case_list)))
        
    for Case in case_list:
        
        if Case in TDownsampledCases:
            df_read = pd.read_csv(f'/home/csi20local/Data/RG_CT_Cases/{Case}/csv_results/MT-HiRes-TDownsampled-{Error}.csv', 
                        sep = ' ', index_col = 0)
            df_array = df_read.to_numpy() 
            flattened_array = np.reshape(df_array, 63) # flatten array to 1D array with 63 elements
    
            cases_array[:, case_list.index(Case)] = flattened_array # assign flattened array to corresponding case col.
    
        else:
            df_read = pd.read_csv(f'/home/csi20local/Data/RG_CT_Cases/{Case}/csv_results/MT-HiRes-{Error}.csv', 
                        sep = ' ', index_col = 0)
            df_array = df_read.to_numpy()
            flattened_array = np.reshape(df_array, 63)
                
            cases_array[:, case_list.index(Case)] = flattened_array
                
    # Create array for medians of errors for each (SE, BE) combo across cases
    medians = np.zeros(63)

    for i in range(0,cases_array.shape[0]):
        # Take median across case columns for each (SW,BE) participant and assign to medians array
        medians[i] = np.median(cases_array[i, :])
            
    # Find mean and std dev of medians across 63 (SW, BE) combinations
    mean = np.mean(medians)
    std = np.std(medians)
        
    BE_rename = {0: 4e-6, 1: 1e-6, 2: 4e-7, 3: 1e-7, 4: 4e-8, 5: 1e-8, 6: 4e-9, 7: 1e-9, 8: 4e-10}
    SW_rename = {0: '9e-2', 1: '3e-2', 2: '9e-3', 3: '3e-3', 4: '9e-4', 5: '3e-4', 6: '0.0'}
  
    # Create Dataframe of Median error for each (SW, BE) combination 
    df_medians = np.reshape(medians, (9,7))
    df_medians = pd.DataFrame(df_medians)
    df_medians = df_medians.rename(index = BE_rename, columns=SW_rename)
    
    # Create Dataframe of Z scores for each (SE, BE) combination
    df_zscore = (df_medians-mean)/std
    df_zscore = df_zscore.rename(index = BE_rename, columns=SW_rename)
    
    if Error == "Dice-Results":
        
        # Correct mean and medians in the case of minimising DSC means improving segmentation
        mean = 1 - mean
        df_medians = 1 - df_medians
        
        df_zscore = (df_medians-mean)/std
#         df_zscore = 1 - df_zscore # Old code
    
    return mean, std, df_medians, df_zscore

def S_unified_Vxm_WIP(case_list, Error):
    """
    Calculates unified z-score of all lmbda across a provided list of cases for training. 

    INPUT: 
        * List of cases
        * Error type.

    OUTPUT: 
        * Mean, std deviation, DataFrame of medians (across cases) of each hyperparameter combination, DataFrame of
            z score of each hyperparameter combination across cases
    """
    
    # Dict to convert error nickname to csv filename
    error_dict = {'ASD': 'Normal-Distance-Results', 'DHD': 'Hausdorff-Distance-Results', 'Dice': 'Dice-Results'}
    
    Error = error_dict[Error]
    
    # Create array to hold errors across cases for each (SW,BE) participant
    cases_array = np.zeros(shape=(63,len(case_list)))
    
    # Create list of cases with 20 time frames
    TDownsampledCases = ['21', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '34']
    TDownsampledCases = ['CT-CRT-' + case for case in TDownsampledCases]
    TDownsampledCases_add = ['EBR-01', 'EBR-02']
    TDownsampledCases = TDownsampledCases + TDownsampledCases_add
        
    for Case in case_list:
        
        if Case in TDownsampledCases:
            df_read = pd.read_csv(f'/home/csi20/Dropbox/phd/Data/RG_CT_Cases/{Case}/csv_results/MT-HiRes-TDownsampled-{Error}.csv', 
                        sep = ' ', index_col = 0)
            df_array = df_read.to_numpy() 
            flattened_array = np.reshape(df_array, 63) # flatten array to 1D array with 63 elements
    
            cases_array[:, case_list.index(Case)] = flattened_array # assign flattened array to corresponding case col.
    
        else:
            df_read = pd.read_csv(f'/home/csi20/Dropbox/phd/Data/RG_CT_Cases/{Case}/csv_results/MT-HiRes-{Error}.csv', 
                        sep = ' ', index_col = 0)
            df_array = df_read.to_numpy()
            flattened_array = np.reshape(df_array, 63)
                
            cases_array[:, case_list.index(Case)] = flattened_array
                
    # Create array for medians of errors for each (SE, BE) combo across cases
    medians = np.zeros(63)

    for i in range(0,cases_array.shape[0]):
        # Take median across case columns for each (SW,BE) participant and assign to medians array
        medians[i] = np.median(cases_array[i, :])
            
    # Find mean and std dev of medians across 63 (SW, BE) combinations
    mean = np.mean(medians)
    std = np.std(medians)
        
    BE_rename = {0: 4e-6, 1: 1e-6, 2: 4e-7, 3: 1e-7, 4: 4e-8, 5: 1e-8, 6: 4e-9, 7: 1e-9, 8: 4e-10}
    SW_rename = {0: '9e-2', 1: '3e-2', 2: '9e-3', 3: '3e-3', 4: '9e-4', 5: '3e-4', 6: '0.0'}
  
    # Create Dataframe of Median error for each (SW, BE) combination 
    df_medians = np.reshape(medians, (9,7))
    df_medians = pd.DataFrame(df_medians)
    df_medians = df_medians.rename(index = BE_rename, columns=SW_rename)
    
    # Create Dataframe of Z scores for each (SE, BE) combination
    df_zscore = (df_medians-mean)/std
    df_zscore = df_zscore.rename(index = BE_rename, columns=SW_rename)
    
    if Error == "Dice-Results":
        
        # Correct mean and medians in the case of minimising DSC means improving segmentation
        mean = 1 - mean
        df_medians = 1 - df_medians
        
        df_zscore = (df_medians-mean)/std
#         df_zscore = 1 - df_zscore # Old code
    
    return mean, std, df_medians, df_zscore