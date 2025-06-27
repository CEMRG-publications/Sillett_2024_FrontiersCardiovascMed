import pyvista as pv
import argparse
from pathlib import Path
import pandas as pd
import numpy as np

## Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--msh', required=True, help='path to msh you want to append strains to, e.g. cLr-fibres-aligned-4.vtp')
parser.add_argument('--lng-strains', required=True, help='path to lng strains e.g. lng_circ-strains-t10.txt')
# parser.add_argument('--squeez', required=True, help='path to squeez strains file e.g. squeez-4.csv')
# parser.add_argument('--squeez-minus', required=True, help='path to squeez minus strains file e.g. squeez-minus-4.csv')
parser.add_argument('--field_name', default='lng-strains', help='name of field data to save. Default: lng-strains')
args = parser.parse_args()

## Read msh
msh = pv.read(args.msh)

## Read in strains as a df
lng_strains_df = pd.read_csv(f'{args.lng_strains}', 
		sep=' ', skiprows=2, names=['lng', 'crc', 'n'])

long_strain_data = lng_strains_df['lng']

## Convert Green strain to linear strain
data=np.sqrt(2*long_strain_data+1)-1
data=data*100

## Convert to numpy arrays and append to msh
msh.cell_data[args.field_name] = data.to_numpy()
# msh.cell_data["squeez"] = squeez['Area'].to_numpy()
# msh.cell_data["squeez_minus"] = squeez_minus['Area'].to_numpy()

# Save msh
msh_pl = Path(args.msh)
msh.save(f"{msh_pl.parent}/{msh_pl.name}")