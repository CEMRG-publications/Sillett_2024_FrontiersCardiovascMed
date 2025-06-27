import argparse
import pyvista as pv
import numpy as np

## Generate_Region_Labels.py

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate 5 regional labels for LA msh (Roof, septum, lateral wall, anterior wall, posterior wall')
	parser.add_argument('--filepath', required=True, help='CemrgApp Fibres project directory with the 2D UAC msh and output msh from CemrgApp Fibres pipeline', default='./')
	parser.add_argument('--UAC-name', help='Name of saved UAC msh with regional labels.', default='LCoords_2D_R_v3_C-regional_labels')
	parser.add_argument('--LA-name', help='Name of saved LA msh with regional labels.', default='cLr-regional_labels')
	args = parser.parse_args()

	
    ## Read in 2D UAC and LA msh
	uac_msh = pv.read(f"{args.filepath}/Labelled_Coords_2D_Rescaling_v3_C.vtk")
	la_msh = pv.read(f"{args.filepath}/clean-Labelled-refined.vtk")

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

	uac_msh.cell_data["region_label"] = local_region_ar
	la_msh.cell_data["region_label"] = local_region_ar

	## Save mshes with regional labels
	uac_msh.save(f"{args.filepath}/{args.UAC_name}.vtk")
	la_msh.save(f"{args.filepath}/{args.LA_name}.vtk")