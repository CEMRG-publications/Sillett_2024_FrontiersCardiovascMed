### Use this script to read in .vtk files and save as .vtu

import sys
import argparse
import pyvista as pv
from pathlib import Path

## parse arguments
parser = argparse.ArgumentParser()

parser.add_argument('--vtk-msh', required=True, help='path to .vtk msh to convert to .vtu')

args = parser.parse_args()

msh = pv.read(args.vtk_msh)

## Get Save path
vtk_msh_pl = Path(args.vtk_msh)

print(f'Saving at: {vtk_msh_pl.parent}/{vtk_msh_pl.stem}.vtu')
msh.save(f'{vtk_msh_pl.parent}/{vtk_msh_pl.stem}.vtu')