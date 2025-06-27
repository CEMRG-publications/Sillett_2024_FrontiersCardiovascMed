## This script is for calculating surface area strain transients
## For investigating coarsest level of area strain

import pyvista as pv
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import mean_squared_error

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Plot surface area strain transients. Excludes PVs & LAA.')

	parser.add_argument('--case', required=True, help='case to plot strains for')
	parser.add_argument('--file-path', required=True, help='project directory containing all strain .txt files')
	parser.add_argument('--fibres-path', required=True, help='fibres project directory. Only if using --regional flag')
	parser.add_argument('--regional', action='store_true')
	parser.add_argument('--mean', action='store_true')
	parser.add_argument('--squeez', action='store_true')
	parser.add_argument('--save-txt', action='store_true')
	parser.add_argument('--numTimes', help='Total number of time frames [10]', default=10)
	parser.add_argument('--png-out', required=True, help='output .png filename', default='./strain_transient.png')

	args = parser.parse_args()