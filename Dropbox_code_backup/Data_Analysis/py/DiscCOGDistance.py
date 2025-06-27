import pandas as pd
import numpy as np
import sys

def calculate_COG(path2points):
    
    df = pd.read_csv(path2points, skiprows=2, sep = ' ', names=['Point', 'Point ID', 'X', 'Y', 'Z'])
    df = df.drop(['Point'], axis=1)
    
    cog_X = df['X'].sum()/df.shape[0]
    cog_Y = df['Y'].sum()/df.shape[0]
    cog_Z = df['Z'].sum()/df.shape[0]
    
    return cog_X, cog_Y, cog_Z

def distance(tupleA, tupleB):
    
    dx = tupleA[0] - tupleB[0]
    dy = tupleA[1] - tupleB[1]
    dz = tupleA[2] - tupleB[2]
    
    dist_sq = dx**2 + dy**2 + dz**2
    ans = np.sqrt(dist_sq)
    
    return ans

path2dcm4_Disc = str(sys.argv[1])
path2trk_Disc = str(sys.argv[2])

trk = calculate_COG(path2trk_Disc)
dcm4 = calculate_COG(path2dcm4_Disc)

dist = distance(trk, dcm4)

print(dist)