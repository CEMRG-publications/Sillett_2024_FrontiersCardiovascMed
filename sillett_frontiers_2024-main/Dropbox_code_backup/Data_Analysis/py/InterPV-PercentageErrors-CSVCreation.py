import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# This function creates a 5x5 csv file of Inter PVs perctange errors for a given combo of SW and BE
# This was used to create InterPV-PercentageErrors.csv files for all SW BE combos for Cases: '02', '06', '07', '08', '12', '15', '16'

def CSV_Creation_SW_BE_pC_pC_distances(Case, Res, SW, BE):
            
    series_errors = pd.read_csv(f'/home/csi20local/Data/RG_CT_Cases/CT-CRT-{Case}/{Res}/SW-{SW}-BE-{BE}/pC-pC-distances.txt', sep = ' ', names=['Error'])
            
    reshaped_array = np.reshape(series_errors.to_numpy(), (5,5))
    reshaped_array = np.abs(reshaped_array)
    
    SWBE_df_errors = pd.DataFrame(data=reshaped_array, columns=['LAA', 'LS', 'LI', 'RS', 'RI'],
                                  index=['LAA', 'LS', 'LI', 'RS', 'RI'])
    
    SWBE_df_errors.to_csv(f'/home/csi20local/Data/RG_CT_Cases/CT-CRT-{Case}/{Res}/SW-{SW}-BE-{BE}/InterPV-PercentageErrors.csv', sep=' ')

# Function to check csv created for InterPV-PercentageErrors.csv for a given (SW,BE) matches pC-pC-distances.txt
# This was used to check InterPV-PercentageErrors.csv files for all SW BE combos for Cases: '02', '06', '07', '08', '12', '15', '16'

def CHECK_CSV_Creation_SW_BE_pC_pC_distances(Case, SW, BE):
    
    test_reread = pd.read_csv(f'/home/csi20local/Data/RG_CT_Cases/CT-CRT-{Case}/MT-HiRes/SW-{SW}-BE-{BE}/InterPV-PercentageErrors.csv',
                              sep = ' ', index_col = 0)
    test_reread = test_reread.fillna(0.0)
    test_reread_flatten = test_reread.to_numpy().flatten()

    Errors_series = pd.read_csv(f'/home/csi20local/Data/RG_CT_Cases/CT-CRT-{Case}/MT-HiRes/SW-{SW}-BE-{BE}/pC-pC-distances.txt',
                         sep = ' ', names=['Error'])
    Errors_series = Errors_series.fillna(0.0)
    
    status=True

    for i in range(0, Errors_series.shape[0]):
                
        if np.abs(round(Errors_series.iloc[i][0],6)) != round(test_reread_flatten[i],6):
            print(f"Entry {i} of Case {Case}, SW {SW}, BE {BE} has problem")
            status=False
            break
        
    return print(status)

# This function creates a 9x7 csv table of Inter PVs percentage errors for a given PV1-PV2 combination across
# all (SW,BE) combinations

def CSV_Creation_PV1_PV2_pC_pC_distances(Case, Res, PV1, PV2):
    
    PV1_PV2 = []
    
    for BE in ['4e-6', '1e-6', '4e-7', '1e-7', '4e-8', '1e-8', '4e-9', '1e-9', '4e-10']:
        for SW in ['9e-2', '3e-2', '9e-3', '3e-3', '9e-4', '3e-4', '0.0']:
            
            reread = pd.read_csv(f'/home/csi20local/Data/RG_CT_Cases/CT-CRT-{Case}/MT-HiRes/SW-{SW}-BE-{BE}/InterPV-PercentageErrors.csv',
                                 sep = ' ', index_col = 0)
            
            PV1_PV2.append(reread.loc[f"{PV1}"][f"{PV2}"])
            
    reshaped_array = np.reshape(np.array(PV1_PV2), (9,7))
    reshaped_array = np.abs(reshaped_array)
    
    df = pd.DataFrame(reshaped_array, columns=['9e-2', '3e-2', '9e-3', '3e-3', '9e-4', '3e-4', '0.0'], 
             index=['4e-6', '1e-6', '4e-7', '1e-7', '4e-8', '1e-8', '4e-9', '1e-9', '4e-10'])
    
    df.to_csv(f'/home/csi20local/Data/RG_CT_Cases/CT-CRT-{Case}/{PV1}-{PV2}-PercentageErrors.csv', sep=' ')

## This function checks the CSV file created for InterPV percentage errors 

def CHECK_CSV_Creation_PV1_PV2_pC_pC_distances(Case, Res, PV1, PV2):
    
    PV1PV2_csv = pd.read_csv(f"/home/csi20local/Data/RG_CT_Cases/CT-CRT-{Case}/{PV1}-{PV2}-PercentageErrors.csv",
                            sep=' ', index_col=0)
    
    status = True
    
    for BE in ['4e-6', '1e-6', '4e-7', '1e-7', '4e-8', '1e-8', '4e-9', '1e-9', '4e-10']:
        for SW in ['9e-2', '3e-2', '9e-3', '3e-3', '9e-4', '3e-4', '0.0']:
            
            SWBE_df = pd.read_csv(f"/home/csi20local/Data/RG_CT_Cases/CT-CRT-{Case}/MT-HiRes/SW-{SW}-BE-{BE}/InterPV-PercentageErrors.csv",
                                      sep=' ', index_col=0)
                

            if (round(PV1PV2_csv[f'{SW}'][float(BE)], 6) == round(SWBE_df[f'{PV1}'][f'{PV2}'], 6)):
                status = True
                    
            else:
                print(f"Problem with Case {Case}, {PV1}-{PV2} Error at BE {BE} SW {SW}")
                status=False
                break
    

    return print(status)


if __name__ == "__main__":

	# for Case in ['02', '06', '07', '08', '12', '15', '16']:
	    
	#     print(Case)

	#     for SW in ['9e-2', '3e-2', '9e-3', '3e-3', '9e-4', '3e-4', '0.0']:

	#         for BE in ['4e-6', '1e-6', '4e-7', '1e-7', '4e-8', '1e-8', '4e-9', '1e-9', '4e-10']:

	#                 CSV_Creation_SW_BE_pC_pC_distances(Case, "MT-HiRes", SW, BE)


	for Case in ['02', '06', '07', '08', '12', '15', '16']:
		print(Case)

    	for SW in ['9e-2', '3e-2', '9e-3', '3e-3', '9e-4', '3e-4', '0.0']:

            for BE in ['4e-6', '1e-6', '4e-7', '1e-7', '4e-8', '1e-8', '4e-9', '1e-9', '4e-10']:

                CHECK_CSV_Creation_SW_BE_pC_pC_distances(Case, SW, BE)

                

    # for Case in ['02', '06', '07', '08', '12', '15', '16']:
    # 	print(Case)
    
    # for (PV1,PV2) in [('LAA', 'LS'), ('LAA', 'LI'), ('LAA','RS'), ('LAA','RI'),
    #              ('LS', 'LI'), ('LS', 'RS'), ('LS', 'RI'),
    #              ('LI', 'RS'), ('LI', 'RI'),
    #              ('RS', 'RI')]:
        
    #     CSV_Creation_PV1_PV2_pC_pC_distances(Case, "MT-HiRes", PV1, PV2)


    for Case in ['02', '06', '07', '08', '12', '15', '16']:
    	print(Case)
    
    for (PV1,PV2) in [('LAA', 'LS'), ('LAA', 'LI'), ('LAA','RS'), ('LAA','RI'),
                 ('LS', 'LI'), ('LS', 'RS'), ('LS', 'RI'),
                 ('LI', 'RS'), ('LI', 'RI'),
                 ('RS', 'RI')]:
        
        CHECK_CSV_Creation_PV1_PV2_pC_pC_distances(Case, "MT-HiRes", PV1, PV2)
