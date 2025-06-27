"""
Use this script to edit the area strain colourmap such that PVs are labelled with NaN
"""

import pyvista as pv
import numpy as np
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--trk-msh', help='tracked mesh with strains e.g. cLr-fibres-aligned-4.vtp', required=True)
parser.add_argument('--uac-msh', help='mesh with regions. e.g. cLr-regional_labels.vtk', required=True)
args = parser.parse_args()

msh = pv.read(args.trk_msh)
region_msh = pv.read(args.uac_msh)

regions = region_msh.cell_data["region_label_v2"]

## Remove PVs from Area Strains
data = msh.cell_data["area-strains"].copy()
data[[regions == 0.0]] = np.nan
msh.cell_data["area-strains-woPVs"] = data

## Remove PVs from Fibre Strains
data = msh.cell_data["endo_avg-f1_strains"].copy()
data[[regions == 0.0]] = np.nan
msh.cell_data["endo_avg-f1_strains-woPVs"] = data

## Remove Fibre Glyphs 
## Choose Scale Array as new field below
data = msh.cell_data['endo_avg'].copy()
data[[regions == 0.0]] = 0.0
msh.cell_data["endo_avg-woPVs"] = data

## Save mesh
trk_msh_pl = Path(args.trk_msh)

msh.save(f"{trk_msh_pl.parent}/{trk_msh_pl.stem}.vtp")
msh.save(f"{trk_msh_pl.parent}/{trk_msh_pl.stem}.vtk")