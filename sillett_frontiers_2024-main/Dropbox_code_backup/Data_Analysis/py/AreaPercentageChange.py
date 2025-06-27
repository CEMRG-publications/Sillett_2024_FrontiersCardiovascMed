import numpy as np
import pandas as pd
import sys

OriginalAreas = str(sys.argv[1])
TrackedAreas = str(sys.argv[2])

def PercentageAreaChange(Path2OriginalMesh, Path2TrackedMesh):
    
    df_dcm0 = pd.read_csv(Path2OriginalMesh, delim_whitespace=True, skiprows=1, 
                          names = ['Cell', 'Cell Number', 'Ar', 'Area'])
    
    df_tracked = pd.read_csv(Path2TrackedMesh, delim_whitespace=True, skiprows=1, 
                             names = ['Cell', 'Cell Number', 'Ar', 'Area'])
    
    ans = (df_tracked['Area'] - df_dcm0['Area'])/df_dcm0['Area'] * 100
    
    return ans

area_change = PercentageAreaChange(OriginalAreas, TrackedAreas)

print(area_change)

## HOW TO accomodate for paraview format for colouring mesh???