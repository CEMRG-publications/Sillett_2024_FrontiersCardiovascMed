## FROM ipython jupyter notebook AreaPercentageChange Attempt

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

if len(sys.argv) != 4:
  print("Usage: " + sys.argv[0] + " Path to dcm0 cell areas; Path to tracked mesh cell areas; Frame")
  sys.exit(1)

# Load arguments
dcm0_areas_path = str(sys.argv[1])
tracked_areas_path = str(sys.argv[2])
tracked_frame = str(sys.argv[3])

def AreaStrain(Path2dcm0Areas, Path2trackedAreas, frame):
    
    df_dcm0 = pd.read_csv(Path2dcm0Areas, delim_whitespace=True, skiprows=1, 
                          names = ['Cell', 'Cell Number', 'Area_label', 'Area'])
    
    df_tracked = pd.read_csv(Path2trackedAreas, delim_whitespace=True, skiprows=1, 
                             names = ['Cell', 'Cell Number', 'Area_label', 'Area'])
    
    ans = (df_tracked['Area'] - df_dcm0['Area'])/df_dcm0['Area']
    
    ans.to_csv(os.path.dirname(Path2trackedAreas) + f'/area-strains-{frame}.csv', header=True)
    
    return ans


def AbsoluteAreaStrain(Path2dcm0Areas, Path2trackedAreas):
    
    df_dcm0 = pd.read_csv(Path2dcm0Areas, delim_whitespace=True, skiprows=1, 
                          names = ['Cell', 'Cell Number', 'Area_label', 'Area'])
    
    df_tracked = pd.read_csv(Path2trackedAreas, delim_whitespace=True, skiprows=1, 
                             names = ['Cell', 'Cell Number', 'Area_label', 'Area'])
    
    ans = (df_tracked['Area'] - df_dcm0['Area'])/df_dcm0['Area']
    
    ans = ans.abs()
    
    ans.to_csv(os.path.dirname(Path2trackedAreas) + '/absolute-area-strains.csv', header=True)
    
    return ans


AreaStrain(dcm0_areas_path, tracked_areas_path, tracked_frame)