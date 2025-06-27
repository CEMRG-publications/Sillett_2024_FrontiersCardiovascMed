
"""
Use this script to run the LA motion tracking pipeline step by step. 

Previously shared with Bei for implementation in CemrgApp

Requirements:
    * CemrgApp MIRTK executables, located in bin/MLib
    * vtk virtual environment. See vtk-env.txt for dependencies
"""

import os, sys
import pandas as pd

case=sys.argv[1]

# Define basePath for data location
basePath="/media/cs1623/Elements/Vitaliy_BiV"

cropImages=False
registration=False
deformMesh=False
generateCellAreaStrains=False
jacobianThreshold=False
plotAreaStrain=False
calcFiberStrains=False
plotFiberStrains=False
createOverlays=False

# cropImages=True
# registration=True
# deformMesh=True
# generateCellAreaStrains=True
# jacobianThreshold=True
# plotAreaStrain=True
# calcFiberStrains=True
# plotFiberStrains=True

print(f"**************** {case} ****************")

# Define used paths
casePath=f"{basePath}/{case}"
niftiPath=f"{casePath}/nifti"
# uacFolder="UAC_CT"
uacFolder="LA/UAC_CT"
uacPath=f"{casePath}/{uacFolder}"
# trackingFolder="MT/SW-0.0-BE-1e-9"
trackingFolder="LA/MT/SW-0.0-BE-1e-9"
trackingPath=f"{casePath}/{trackingFolder}"
print(trackingPath)

# Define number of image frames used for tracking
numTimes=20

if cropImages:
    print("############################################################ Crop nifti images!!! ######################################################")

    ## Read in excel file containing cropping dimensions
    path2cropping_info=f"/home/csi20/Projects_Local/sillett_frontiers_2024/la_strain_pipeline/param_files/LA-cropping.xlsx"
    df=pd.read_excel(path2cropping_info)
    print(df)
    i = df.index[df['Case']==case][0]
    x_start = df.loc[i, "x_start"]
    y_start = df.loc[i, "y_start"]
    z_start = df.loc[i, "z_start"]

    x_end = df.loc[i, "x_end"]
    y_end = df.loc[i, "y_end"]
    z_end = df.loc[i, "z_end"]

    cmd=f"bash /home/csi20/Projects_Local/sillett_frontiers_2024/la_strain_pipeline/img_analysis_scripts/sh/CropNiftiLoop.sh {niftiPath} {x_start} {y_start} {z_start} {x_end} {y_end} {z_end}"
    print(cmd)
    os.system(cmd)

if registration:
    print("############################################################ Doing the image registration!!! ######################################################")
    
    # Generate Final.CFG file using the optimal hyperparameters found in Frontiers 2024 paper Sillett et al.
    cmd=f"/home/csi20/Projects_Local/sillett_frontiers_2024/la_strain_pipeline/img_analysis_scripts/sh/GenerateCFG.sh 1e-9 0.0"
    cmd+=f" > {trackingPath}/Final.cfg"

    print(cmd)
    # os.system(cmd)

    # Generate imgTimes.lst file
    cmd=f"/home/csi20/Projects_Local/sillett_frontiers_2024/la_strain_pipeline/img_analysis_scripts/sh/GenerateLST_20_TDownsampled.sh"
    cmd+=f" > {trackingPath}/imgTimes.lst"

    print(cmd)
    # os.system(cmd)
    
    # Registration using MIRTK
    cmd=f"/home/csi20/Software/CemrgApp_v2.1/bin/MLib/register"
    cmd+=f" -images {trackingPath}/imgTimes.lst"
    cmd+=f" -parin {trackingPath}/Final.cfg"
    cmd+=f" -dofout {trackingPath}/tsffd.dof"
    cmd+=f" -threads 20 -verbose 3"

    print(cmd)
    os.system(cmd)

if deformMesh:
    print(f"############################################################ Deforming Mesh!!! ############################################################")

    for frame in range(numTimes):

        cmd=f"/home/csi20/Software/CemrgApp_v2.1/bin/MLib/transform-points"
        cmd+=f" {uacPath}/clean-Labelled-refined-aligned.vtp"
        cmd+=f" {trackingPath}/cLr-aligned-{frame}.vtp"
        cmd+=f" -dofin {trackingPath}/tsffd.dof -ascii -St {frame}0 -verbose 3"

        print(cmd)
        os.system(cmd)

if generateCellAreaStrains:
    print("################# Generate Cell Area Strains ###################")

    cmd=f"bash /home/csi20/Projects_Local/sillett_frontiers_2024/la_strain_pipeline/img_analysis_scripts/sh/la_area_csvCreation-20f.sh {case} {uacPath} {trackingPath}"

    print(cmd)
    os.system(cmd)

if jacobianThreshold:
    print("################# Generate Jacobian Threshold ###################")

    cmd=f"/home/csi20/anaconda3/envs/vtk/bin/python /home/csi20/Projects_Local/sillett_frontiers_2024/la_strain_pipeline/img_analysis_scripts/py/print_mesh_qual.py"
    cmd+=f" --case {case}"
    cmd+=f" --file-path {trackingFolder}"
    cmd+=f" --numTimes {numTimes}"

    print(cmd)
    os.system(cmd)

if plotAreaStrain:
    print("################# Plotting Area Strain Transients ###################")

    ## Global strain plot
    cmd=f"/home/csi20/anaconda3/envs/vtk/bin/python /home/csi20/Projects_Local/sillett_frontiers_2024/la_strain_pipeline/img_analysis_scripts/py/plot_areastrain_transients_mshqual.py"
    cmd+=f" --case {case}"
    cmd+=f" --file-path {trackingFolder}"
    cmd+=f" --fibres-path {uacFolder}"
    cmd+=f" --numTimes {numTimes}"
    cmd+=f" --save-txt"

    print(cmd)
    os.system(cmd)

    ## Regional strain plot
    cmd=f"/home/csi20/anaconda3/envs/vtk/bin/python /home/csi20/Projects_Local/sillett_frontiers_2024/la_strain_pipeline/img_analysis_scripts/py/plot_areastrain_transients_mshqual.py"
    cmd+=f" --case {case}"
    cmd+=f" --file-path {trackingFolder}"
    cmd+=f" --fibres-path {uacFolder}"
    cmd+=f" --numTimes {numTimes}"
    cmd+=f" --regional"
    cmd+=f" --save-txt"

    print(cmd)
    os.system(cmd)
    
if calcFiberStrains:
    print("################# Calculate Fibre Strains ###################")

    cmd=f"bash /home/csi20/Projects_Local/sillett_frontiers_2024/la_strain_pipeline/img_analysis_scripts/sh/calculate_fibre_strain.sh {trackingPath} {uacPath} {numTimes}"

    print(cmd)
    os.system(cmd)

if plotFiberStrains:
    print("################# Plotting Fibre Strains ###################")

    ## Global plots
    cmd=f"python /home/csi20/Projects_Local/sillett_frontiers_2024/la_strain_pipeline/img_analysis_scripts/py/plot_fibrestrain_transients_percentiles_mshqual.py"
    cmd+=f" --case {case}"
    cmd+=f" --file-path {trackingFolder}"
    cmd+=f" --fibres-path {uacFolder}"
    cmd+=f" --fibre-arch endo_avg"
    cmd+=f" --save-txt"
    print(cmd)
    os.system(cmd)

    ## Regional plots
    cmd=f"python /home/csi20/Projects_Local/sillett_frontiers_2024/la_strain_pipeline/img_analysis_scripts/py/plot_fibrestrain_transients_percentiles_mshqual.py"
    cmd+=f" --case {case}"
    cmd+=f" --file-path {trackingFolder}"
    cmd+=f" --fibres-path {uacFolder}"
    cmd+=f" --fibre-arch endo_avg"
    cmd+=f" --save-txt"
    cmd+=f" --regional"
    print(cmd)
    os.system(cmd)