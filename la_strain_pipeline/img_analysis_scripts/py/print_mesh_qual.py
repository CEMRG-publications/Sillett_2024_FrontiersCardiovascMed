"""
Use this script to print mesh quality on cell by cell basis.

Print scaled jacobian for each cell.
"""

import pyvista as pv
import argparse
import numpy as np

# DataPath="/media/cs1623/Elements/Vitaliy"
# DataPath="/home/csi20/Data/Vitaliy"
# DataPath="/home/csi20/Data/Vitaliy_Reproducibility"
# DataPath="/media/cs1623/Elements1/Vitaliy_BiV"
DataPath="/home/csi20/Data/VitaliyProject_Tiffany_Reproducibility"

parser = argparse.ArgumentParser()
parser.add_argument('--case', required=True, help='case to plot strains for. e.g. CT-CRT/case01 or DICOMs/S-0400')
parser.add_argument('--file-path', required=True, help='project directory containing all strain .txt files e.g. MT-HiRes/SW-0.0-BE-1e-9')
parser.add_argument('--numTimes', help='Total number of time frames [10]', default=10)
args = parser.parse_args()

for i in range(1, int(args.numTimes)):
    print(i)
    
    ## Read msh
    # msh = pv.read(f'{DataPath}/{args.case}/{args.file_path}/cLr-fibres-aligned-{i}.vtp')
    msh = pv.read(f'{DataPath}/{args.case}/{args.file_path}/cLr-aligned-{i}.vtp')
    
    ## Calc and get scaled jacobian per cell
    qual = msh.compute_cell_quality(quality_measure="scaled_jacobian")
    CellQuality = qual.get_array("CellQuality")

    ## Calc percentage of cells above threshold
    thresh=0.2
    fail_percent=(CellQuality>thresh).sum()/CellQuality.size
    print(fail_percent)

    np.savetxt(f"{DataPath}/{args.case}/{args.file_path}/cLr-fibres-aligned-{i}-scal_jacob-thr0.2.txt", CellQuality)