## Script to align fibre mesh to original mesh

"""
Before applying transform-points to LA model outputted from CemrgApp Atrial Fibres pipeline, the output mesh (clean-Labelled-refined.vtk)
 must be aligned in space with the original mesh (LA-msh.vtk) used as input.

This script attempts to autoamte this process but is not perfect. For quick verification of output, check alignment of meshes in Paraview. 
"""

import pyvista as pv
import numpy as np
import argparse
from pathlib import Path

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--cLr', required=True, help='path to fibre mesh want to transform. E.g. clean-Labelled-refined.vtk')
parser.add_argument('--seg-msh', required=True, help='path to unclipped fibre msh. E.g: UAC_CT_aligned/segmentation-rot.vtk')
parser.add_argument('--og-msh', required=True, help='path to original mesh used as first input to UAC pipeline. E.g. LA-msh.vtk')
args = parser.parse_args()

# Read meshes
cLr_msh = pv.read(args.cLr)
seg_msh = pv.read(args.seg_msh)
og_msh = pv.read(args.og_msh)

# Centres of Mass
seg_msh_com = seg_msh.center_of_mass()
og_com = og_msh.center_of_mass()

# Transform 
translate = og_com - seg_msh_com

# Numpy array
transform = np.array([[1, 0, 0, translate[0]],
                [0, 1, 0, translate[1]],
                [0, 0, 1, translate[2]],
                [0, 0, 0, 1]])

# Apply transform
aligned_msh = cLr_msh.transform(transform)

# Save
cLr_pl = Path(args.cLr)
aligned_msh.save(f'{cLr_pl.parent}/{cLr_pl.stem}-aligned.vtk')
aligned_msh.save(f'{cLr_pl.parent}/{cLr_pl.stem}-aligned.vtp')