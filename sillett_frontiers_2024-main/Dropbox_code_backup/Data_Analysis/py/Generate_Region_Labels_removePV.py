import argparse
import pyvista as pv
import numpy as np

## Generate_Region_Labels_removePVs.py

"""
This script is for assigning generating 5 regional labels for the LA.

Requires LA msh and its corresponding UAC unit square outputs from CemrgApp UAC pipeline.
"""


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate 5 regional labels for LA msh (Roof, septum, lateral wall, anterior wall, posterior wall')
	parser.add_argument('--filepath', required=True, help='CemrgApp Fibres project directory with the 2D UAC msh and output msh from CemrgApp Fibres pipeline', default='./')
	parser.add_argument('--UAC-name', help='Name of saved UAC msh with regional labels.', default='LCoords_2D_R_v3_C-regional_labels')
	parser.add_argument('--LA-name', help='Name of saved LA msh with regional labels.', default='cLr-regional_labels')
	args = parser.parse_args()

	
    ## Read in 2D UAC and corresponding LA msh
	# uac_msh = pv.read(f"{args.filepath}/Labelled_Coords_2D_Rescaling_v3_C.vtk")
	# la_msh = pv.read(f"{args.filepath}/clean-Labelled-refined.vtk")
	# uac_msh = pv.read(f"{args.filepath}/LCoords_2D_R_v3_C-regional_labels.vtk")
	uac_msh = pv.read(f"{args.filepath}/Labelled_Coords_2D_Rescaling_v3_C_copy-p2p-ALL-cells.vtk")

	# la_msh = pv.read(f"{args.filepath}/cLr-regional_labels.vtk")
	la_msh = pv.read(f"{args.filepath}/clean-Labelled-refined-aligned_ManualTranslate-p2p-ALL-cells.vtk")

	## Get upper/lower RH/LH bounds
	## extract veins
	lipv = uac_msh.extract_cells(uac_msh['data']==13)
	rspv = uac_msh.extract_cells(uac_msh['data']==15)

	## bounds
	lower_bound = lipv.center[1] ## ymin
	left_bound = lipv.center[0]  ## xmax

	upper_bound = rspv.center[1]  ## ymax
	right_bound = rspv.center[0]  ## xmin

	## Get region cell IDs
	roof_inds = uac_msh.find_cells_within_bounds([right_bound, left_bound, lower_bound, upper_bound, 0.0, 0.0])
	lat_inds = uac_msh.find_cells_within_bounds([left_bound, 1.0, 0.0, 1.0, 0.0, 0.0])
	sept_inds = uac_msh.find_cells_within_bounds([0.0, right_bound, 0.0, 1.0, 0.0, 0.0])
	post_inds = uac_msh.find_cells_within_bounds([right_bound, left_bound, 0.0, lower_bound, 0.0, 0.0])
	ant_inds = uac_msh.find_cells_within_bounds([right_bound, left_bound, upper_bound, 1.0, 0.0, 0.0])

	## Append cell_data to 2D UAC and LA msh
	local_region_ar = np.zeros((uac_msh.number_of_cells,))

	local_region_ar[roof_inds] = 1.0
	local_region_ar[sept_inds] = 2.0
	local_region_ar[lat_inds] = 3.0
	local_region_ar[ant_inds] = 4.0
	local_region_ar[post_inds] = 5.0

	## Remove PV and LAA inds
	local_region_ar[uac_msh['data']==11] = 0.0
	local_region_ar[uac_msh['data']==13] = 0.0
	local_region_ar[uac_msh['data']==15] = 0.0
	local_region_ar[uac_msh['data']==17] = 0.0
	local_region_ar[uac_msh['data']==19] = 0.0

	# lspv = uac_msh.extract_cells(uac_msh['data']==11)
	# ripv = uac_msh.extract_cells(uac_msh['data']==17)
	# laa = uac_msh.extract_cells(uac_msh['data']==19)

	uac_msh.cell_data["region_label_v2"] = local_region_ar
	la_msh.cell_data["region_label_v2"] = local_region_ar

	## Save mshes with regional labels
	# uac_msh.save(f"{args.filepath}/{args.UAC_name}.vtk")
	# la_msh.save(f"{args.filepath}/{args.LA_name}.vtk")
	uac_msh.save(f"{args.filepath}/Labelled_Coords_2D_Rescaling_v3_C_copy-p2p-ALL-cells.vtk")
	la_msh.save(f"{args.filepath}/clean-Labelled-refined-aligned_ManualTranslate-p2p-ALL-cells.vtk")