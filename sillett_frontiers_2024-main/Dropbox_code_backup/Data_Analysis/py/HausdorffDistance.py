import pandas as pd
import numpy as np
import sys
from scipy.spatial.distance import directed_hausdorff
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--tracked-vertices', required=True, help='path to vertex points of tracked msh')
parser.add_argument('--GT-vertices', required=True, help='path to vertex points of GT msh')

args = parser.parse_args()

# TrackedVertexPoint = str(sys.argv[1])
# RefVertexPoints = str(sys.argv[2])

TrackedVertexPoint = args.tracked_vertices
RefVertexPoints = args.GT_vertices

# print('Tracked mesh Vertex Points ', TrackedVertexPoint, '\n')
# print('Reference mesh Vertex Points ', RefVertexPoints, '\n')

def hausdorff_distance(Path2MshA_Points, Path2MshB_Points):
    MshAPoints = np.genfromtxt(Path2MshA_Points, delimiter=' ', usecols = (2,3,4))
    MshBPoints = np.genfromtxt(Path2MshB_Points, delimiter=' ', usecols = (2,3,4))
    
    forward_hausdorff = directed_hausdorff(MshAPoints, MshBPoints)
    backward_hausdorff = directed_hausdorff(MshBPoints, MshAPoints)
    
    general = max(forward_hausdorff[0], backward_hausdorff[0])
    directed = forward_hausdorff[0]
    
    return general, directed

direct_hausdorff_dist = hausdorff_distance(TrackedVertexPoint, RefVertexPoints)[1]

print(direct_hausdorff_dist)