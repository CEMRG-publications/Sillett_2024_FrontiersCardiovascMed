## Script to append endo and epi fibres to a mesh

import pyvista as pv
import argparse
import pandas as pd
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument('--msh', required=True, help='path to msh you want to append fibre vectors to e.g. clean-Labelled-refined.vtk')
parser.add_argument('--epi-fibres', required=True, help='path to epi fibre vectors you want to append to msh. Name: Labelled_Epi.lon')
parser.add_argument('--endo-fibres', required=True, help='path to endo fibre vectors you want to append to msh. Name: Labelled_Endo.lon')
parser.add_argument('--epi-name', required=True, help='cell_data name to give epi fibres. e.g. epi_1')
parser.add_argument('--endo-name', required=True, help='cell_data name to give endo fibres. e.g. endo_1')

args = parser.parse_args()

# Read msh
msh = pv.read(args.msh)

# Read in fibre vectors
endo_fibres = pd.read_csv(args.endo_fibres, names=['fx', 'fy', 'fz'], sep=' ')
epi_fibres = pd.read_csv(args.epi_fibres, names=['fx', 'fy', 'fz'], sep=' ')
endo_fibres_ar = endo_fibres.to_numpy()
epi_fibres_ar = epi_fibres.to_numpy()

# Append fibre vectors to msh cell data
msh.cell_data[f"{args.endo_name}"] = endo_fibres_ar
msh.cell_data[f"{args.epi_name}"] = epi_fibres_ar

# Save msh
msh_pl = Path(args.msh)
msh.save(f"{msh_pl.parent}/{msh_pl.name}")