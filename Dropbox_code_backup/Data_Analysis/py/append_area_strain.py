import pyvista as pv
import argparse
from pathlib import Path
import pandas as pd

## Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--msh', required=True, help='path to msh you want to append strains to, e.g. cLr-fibres-aligned-4.vtp')
parser.add_argument('--area-strains', required=True, help='path to area strains e.g. area-strains-4.csv')
# parser.add_argument('--squeez', required=True, help='path to squeez strains file e.g. squeez-4.csv')
# parser.add_argument('--squeez-minus', required=True, help='path to squeez minus strains file e.g. squeez-minus-4.csv')
parser.add_argument('--field_name', default='area-strains', help='name of field data to save. Default: area-strains')
args = parser.parse_args()

## Read msh
msh = pv.read(args.msh)

## Read in strains .csv data
area_strains = pd.read_csv(args.area_strains)
# squeez = pd.read_csv(args.squeez)
# squeez_minus = pd.read_csv(args.squeez_minus)

## Convert to numpy arrays and append to msh
msh.cell_data[args.field_name] = 100*area_strains['Area'].to_numpy()
# msh.cell_data["squeez"] = squeez['Area'].to_numpy()
# msh.cell_data["squeez_minus"] = squeez_minus['Area'].to_numpy()

# Save msh
msh_pl = Path(args.msh)
msh.save(f"{msh_pl.parent}/{msh_pl.name}")