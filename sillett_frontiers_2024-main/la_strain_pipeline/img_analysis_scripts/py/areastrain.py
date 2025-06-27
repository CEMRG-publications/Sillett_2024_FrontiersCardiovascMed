import os
import pandas as pd
import argparse
import numpy as np

'''
AreaStrain function: calculates area strain for a pair of area txt files.

Saves to area-strains.csv file in directory of 2nd area.txt file

IDEA: add argument to both functions which denotes target frame number. So can save as areastrains-4.csv for ED - ES strains.
Number for area strains should be the same number for transformed-NUMBER-mesh.vtu 
'''


def AreaStrain(Path2dcm0Areas, Path2trackedAreas, StrainSuffixNum):
    
    df_dcm0 = pd.read_csv(Path2dcm0Areas, delim_whitespace=True, skiprows=1, 
                          names = ['Cell', 'Cell Number', 'Area_label', 'Area'])
    
    df_tracked = pd.read_csv(Path2trackedAreas, delim_whitespace=True, skiprows=1, 
                             names = ['Cell', 'Cell Number', 'Area_label', 'Area'])
    
    ans = (df_tracked['Area'] - df_dcm0['Area'])/df_dcm0['Area']
    
    ans.to_csv(os.path.dirname(Path2trackedAreas) + f'/area-strains-{StrainSuffixNum}.csv', header=True)
    
    return ans

def AreaStrain_wrtConfig(Path2dcm0Areas, Path2trackedAreas, StrainSuffixNum, ConfigurationNum):

    """
    Specify configuraiton you are claculating strains wrt

    """
    
    df_dcm0 = pd.read_csv(Path2dcm0Areas, delim_whitespace=True, skiprows=1, 
                          names = ['Cell', 'Cell Number', 'Area_label', 'Area'])
    
    df_tracked = pd.read_csv(Path2trackedAreas, delim_whitespace=True, skiprows=1, 
                             names = ['Cell', 'Cell Number', 'Area_label', 'Area'])
    
    ans = (df_tracked['Area'] - df_dcm0['Area'])/df_dcm0['Area']
    
    ans.to_csv(os.path.dirname(Path2trackedAreas) + f'/area-strains-{StrainSuffixNum}-wrt-t{ConfigurationNum}.csv', header=True)
    
    return ans

'''
AbsoluteAreaStrain function: calculates absolute area strain for a pair of area txt files.

Saves to absolute-area-strains.csv file in directory of 2nd area.txt file
'''

def AbsoluteAreaStrain(Path2dcm0Areas, Path2trackedAreas, StrainSuffixNum):
    
    df_dcm0 = pd.read_csv(Path2dcm0Areas, delim_whitespace=True, skiprows=1, 
                          names = ['Cell', 'Cell Number', 'Area_label', 'Area'])
    
    df_tracked = pd.read_csv(Path2trackedAreas, delim_whitespace=True, skiprows=1, 
                             names = ['Cell', 'Cell Number', 'Area_label', 'Area'])
    
    ans = (df_tracked['Area'] - df_dcm0['Area'])/df_dcm0['Area']
    
    ans = ans.abs()
    
    ans.to_csv(os.path.dirname(Path2trackedAreas) + f'/absolute-area-strains-{StrainSuffixNum}.csv', header=True)
    
    return ans

'''
SQUEEZ function: calculates SQUEEZ strain for a pair of area txt files.

Saves to absolute-area-strains.csv file in directory of 2nd area.txt file
'''

def SQUEEZ(Path2dcm0Areas, Path2trackedAreas, StrainSuffixNum):
    
    df_dcm0 = pd.read_csv(Path2dcm0Areas, delim_whitespace=True, skiprows=1, 
                          names = ['Cell', 'Cell Number', 'Area_label', 'Area'])
    
    df_tracked = pd.read_csv(Path2trackedAreas, delim_whitespace=True, skiprows=1, 
                             names = ['Cell', 'Cell Number', 'Area_label', 'Area'])
    
    ans = df_tracked['Area']/df_dcm0['Area']
    ans = np.sqrt(ans)
    
    ans.to_csv(os.path.dirname(Path2trackedAreas) + f'/squeez-{StrainSuffixNum}.csv', header=True)
    
    return ans

'''
SQUEEZ_minus function: calculates SQUEEZ strain minus 1, such that same area gives SQUEEZ_minus of 0.

Saves to absolute-area-strains.csv file in directory of 2nd area.txt file
'''

def SQUEEZ_minus(Path2dcm0Areas, Path2trackedAreas, StrainSuffixNum):
    
    df_dcm0 = pd.read_csv(Path2dcm0Areas, delim_whitespace=True, skiprows=1, 
                          names = ['Cell', 'Cell Number', 'Area_label', 'Area'])
    
    df_tracked = pd.read_csv(Path2trackedAreas, delim_whitespace=True, skiprows=1, 
                             names = ['Cell', 'Cell Number', 'Area_label', 'Area'])
    
    ans = df_tracked['Area']/df_dcm0['Area']
    ans = np.sqrt(ans) - 1
    
    ans.to_csv(os.path.dirname(Path2trackedAreas) + f'/squeez-minus-{StrainSuffixNum}.csv', header=True)
    
    return ans

if __name__ == "__main__":

  parser = argparse.ArgumentParser()

  parser.add_argument('--dcm0-areas', required=True, help='path to reference msh areas')
  parser.add_argument('--trk-areas', required=True, help='path to tracked msh areas')
  parser.add_argument('--strain-frame', required=True, help='frame at which area strains are calculated')
  parser.add_argument('--config-frame',help='frame for confguration mesh, which strains are calculated wrt')

  args = parser.parse_args()

  print("1st areas path ", args.dcm0_areas, " 2nd areas path ", args.trk_areas, " Area strain suffix Num ", args.strain_frame)

  if args.config_frame:
    print("Config Frame argument provided!!!")

    AreaStrain_wrtConfig(args.dcm0_areas, args.trk_areas, args.strain_frame, args.config_frame)
    SQUEEZ(args.dcm0_areas, args.trk_areas, args.strain_frame)
    SQUEEZ_minus(args.dcm0_areas, args.trk_areas, args.strain_frame)

  else:
    print("Config Frame argument not provided, so calculating strain wrt dcm0 seg!")

    AreaStrain(args.dcm0_areas, args.trk_areas, args.strain_frame)
    # SQUEEZ(args.dcm0_areas, args.trk_areas, args.strain_frame)
    # SQUEEZ_minus(args.dcm0_areas, args.trk_areas, args.strain_frame)
