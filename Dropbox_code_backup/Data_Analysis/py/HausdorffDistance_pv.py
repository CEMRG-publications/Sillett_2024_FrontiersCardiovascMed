import pandas as pd
import numpy as np
import sys
from scipy.spatial.distance import directed_hausdorff
import argparse
import pyvista as pv

def hausdorff_distance(Path2MshA_Points, Path2MshB_Points):
    forward_hausdorff = directed_hausdorff(Path2MshA_Points, Path2MshB_Points)
    backward_hausdorff = directed_hausdorff(Path2MshB_Points, Path2MshA_Points)
    
    general = max(forward_hausdorff[0], backward_hausdorff[0])
    directed = forward_hausdorff[0]
    
    return general, directed

if __name__ == "__main__":

	parser = argparse.ArgumentParser()

	parser.add_argument('--tracked-msh', required=True, help='path to tracked msh')
	parser.add_argument('--GT-msh', required=True, help='path to GT msh')

	args = parser.parse_args()

	# TrackedVertexPoint = str(sys.argv[1])
	# RefVertexPoints = str(sys.argv[2])

	trk_msh = pv.read(args.tracked_msh)
	gt_msh = pv.read(args.GT_msh)

	direct_hausdorff_dist = hausdorff_distance(trk_msh.points, gt_msh.points)[1]

	print(direct_hausdorff_dist)