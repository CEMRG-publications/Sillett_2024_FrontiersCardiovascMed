import pandas as pd
import numpy as np
import sys
import os

if len(sys.argv) != 3:
  print("Usage: " + sys.argv[0] + " transformed-NUM-clip-Cell-Centres.txt; normal-intersections-NUM.txt")
  sys.exit(1)

TrackedCellCentres = str(sys.argv[1])
NormalIntersectionPoints = str(sys.argv[2])

# print('Tracked mesh Cell Points ', TrackedCellCentres, '\n')
# print('Intersection Points along normals ', NormalIntersectionPoints, '\n')

def distance_along_normals_csv(Path2CellPoints, Path2Intersections):
    
    # Read in Cell points from the mesh where tracking starts
    dfCellPts = pd.read_csv(Path2CellPoints, delim_whitespace=True, skiprows=2, 
                       names = ['P', 'Cell Number', 'X', 'Y', 'Z'])
    dfCellPts = dfCellPts.drop(['P', 'Cell Number'], axis=1)
    
    # Read in Points of Intersections
    dfInters = pd.read_csv(Path2Intersections, delim_whitespace=True, skiprows=5,
                           names = ['Inter', 'for', 'C', 'Cell Number', 'X', 'Y', 'Z'])
    dfInters = dfInters.drop(['Inter', 'for', 'C', 'Cell Number'], axis=1)

    # Calculate distance
    deltaX = dfInters['X']-dfCellPts['X']
    deltaY = dfInters['Y']-dfCellPts['Y']
    deltaZ = dfInters['Z']-dfCellPts['Z']
    distance_sq = deltaX**2 + deltaY**2 + deltaZ**2
    distance = distance_sq**0.5
    
    # Drop points which intersect more than once
    # distance = distance[dfInters['X'] != 0.0]
    distance[distance > 10.0] = "NaN"  ## Debugged.csv
    
    ans = distance
    
    return ans

def distance_along_normals_debug(Path2CellPoints, Path2Intersections):
    
    # Read in Cell points from the mesh where tracking starts
    dfCellPts = pd.read_csv(Path2CellPoints, delim_whitespace=True, skiprows=2, 
                       names = ['P', 'Cell Number', 'X', 'Y', 'Z'])
    dfCellPts = dfCellPts.drop(['P', 'Cell Number'], axis=1)
    
    # Read in Points of Intersections
    dfInters = pd.read_csv(Path2Intersections, delim_whitespace=True, skiprows=5,
                           names = ['Inter', 'for', 'C', 'Cell Number', 'X', 'Y', 'Z'])
    dfInters = dfInters.drop(['Inter', 'for', 'C', 'Cell Number'], axis=1)
    
    print('CellPoints shape ', dfCellPts.shape)
    print('IntersectionPoints shape ' ,dfInters.shape)

    # Calculate distance
    deltaX = dfInters['X']-dfCellPts['X']
    deltaY = dfInters['Y']-dfCellPts['Y']
    deltaZ = dfInters['Z']-dfCellPts['Z']
    distance_sq = deltaX**2 + deltaY**2 + deltaZ**2
    distance = distance_sq**0.5
    
    print('Distance shape before cull of zeros ', distance.shape)
    
    # Drop points which intersect more than once
    distance = distance[dfInters['X'] != 0.0]
    
    print('Distance shape after cull of zeros ', distance.shape)
    
    #ans = np.mean(distance)
    
    return deltaX, deltaY, dfInters, distance

normals_dist_csv = distance_along_normals_csv(Path2CellPoints=TrackedCellCentres,
                      Path2Intersections=NormalIntersectionPoints)

# print(type(os.path.dirname(TrackedCellCentres)))
# print(os.path.dirname(TrackedCellCentres)+'/cell-normal-distances.csv')

# normals_dist_csv.to_csv('/home/csi20local/Data/MarinaData/CT_Charlie/CT-CRT-05/MT-HiRes/SW-3e-4-BE-1e-9/cell-normal-distances.csv', header=True)
normals_dist_csv.to_csv(os.path.dirname(TrackedCellCentres) + '/cell-normal-distances.csv', header=True)

# print(normals_dist_csv)
# print(type(normals_dist_csv))