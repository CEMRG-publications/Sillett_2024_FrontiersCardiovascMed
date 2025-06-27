"""
This script automates the LA surface mesh model_creation pipeline after completing the semi-automatic steps in the CemrgApp Atrial Fibres pipeline.

The semi-automatic steps in CemrgApp required prior to this:
    * Labelling of PV and LAA extents 
    * Clipping of PVs and LAA. 
"""

import os, sys

case=sys.argv[1]

msh_improvement=False
convert_format=False
autoLM=False
uac_stage1=False
uac_stage2=False
fibre_map=False
generateLabelledMsh=False
appendFibres=False
rotateSegMsh=False
alignMesh=False

# msh_improvement=True
# convert_format=True
# autoLM=True
# uac_stage1=True
# uac_stage2=True
# fibre_map=True
# generateLabelledMsh=True
# appendFibres=True
# rotateSegMsh=True
alignMesh=True

# Define basePath to data
# basePath="/home/csi20/Data/VitaliyProject_Tiffany_Reproducibility"
basePath="/home/csi20/Data/Pipeline_Test_Data"

if msh_improvement:
    print("################# Mesh Improvement: Resampling ###################")

    cmd=f"docker run --rm --volume={basePath}/{case}/LA/UAC_CT:/data alonsojasl/cemrg-meshtool:v1.0 resample surfmesh"
    cmd+=" -msh=Labelled"
    cmd+=" -ifmt=vtk"
    cmd+=" -outmsh=Labelled-refined"
    cmd+=" -ofmt=vtk_polydata"
    cmd+=" -max=0.5"
    cmd+=" -avrg=0.3"
    cmd+=" -min=0.1"
    cmd+=" -surf_corr=0.95"

    print(cmd)
    os.system(cmd)

    print("################# Mesh Improvement: Cleaning ###################")

    cmd=f"docker run --rm --volume={basePath}/{case}/LA/UAC_CT:/data alonsojasl/cemrg-meshtool:v1.0 clean quality"
    cmd+=" -msh=Labelled-refined"
    cmd+=" -ifmt=vtk"
    cmd+=" -outmsh=clean-Labelled-refined"
    cmd+=" -ofmt=vtk_polydata"
    cmd+=" -thr=0.2"
    cmd+=" -smth=0.75"
    cmd+=" -iter=200"

    print(cmd)
    os.system(cmd)

    cmd=f"docker run --rm --volume={basePath}/{case}/LA/UAC_CT:/data alonsojasl/cemrg-meshtool:v1.0 clean quality"
    cmd+=" -msh=clean-Labelled-refined"
    cmd+=" -ifmt=vtk"
    cmd+=" -outmsh=clean-Labelled-refined"
    cmd+=" -ofmt=vtk_polydata"
    cmd+=" -thr=0.1"
    cmd+=" -smth=0.75"
    cmd+=" -iter=200"

    print(cmd)
    os.system(cmd)

if convert_format:
    print("################# Convert Format ###################")

    cmd=f"docker run --rm --volume={basePath}/{case}/LA/UAC_CT:/data alonsojasl/cemrg-meshtool:v1.0 convert"
    cmd+=" -imsh=clean-Labelled-refined"
    cmd+=" -ifmt=vtk"
    cmd+=" -omsh=clean-Labelled-refined"
    cmd+=" -ofmt=carp_txt"
    cmd+=" -scale=1000"

    print(cmd)
    os.system(cmd)

if autoLM:

    print("################# Selecting LA landmarks automatically! ###################")

    ## Requires access to AWCL repo: py_atria

    cmd=f"/home/csi20/anaconda3/envs/py_atria/bin/python /home/csi20/Projects_Local/py_atria_latest/py_atria-main/py_atrial_fibres/main_LA_landmarks.py {basePath}/{case}/LA/UAC_CT clean-Labelled-refined.vtk pvClipper_MV.vtk"

    print(cmd)
    os.system(cmd)

    # Rename file for expected filename in later Docker commands
    cmd=f"mv {basePath}/{case}/LA/UAC_CT/prodRefinedLandmarks.txt {basePath}/{case}/LA/UAC_CT/prodLaRefinedLandmarks.txt"
    print(cmd)
    os.system(cmd)

if uac_stage1:

    print("################# UAC: Stage 1 ###################")

    cmd=f"cp /home/csi20/Projects_Local/sillett_frontiers_2024/la_strain_pipeline/param_files/*.par {basePath}/{case}/LA/UAC_CT"
    print(cmd)
    os.system(cmd)

    cmd=f"docker run --rm --volume={basePath}/{case}/LA/UAC_CT:/data cemrg/uac:latest"
    cmd+=" UAC_1_LA"
    cmd+=" _LA_Endo"
    cmd+=" clean-Labelled-refined"
    cmd+=" 1 19 11 13 15 17 prodLaRefinedLandmarks.txt"

    print(cmd)
    os.system(cmd)

    cmd=f"docker run --rm --volume={basePath}/{case}/LA/UAC_CT:/shared:z"
    cmd+=" --workdir=/shared docker.opencarp.org/opencarp/opencarp:latest"
    cmd+=" openCARP -ellip_use_pt 0 -parab_use_pt 0"
    cmd+=" -parab_options_file /usr/local/lib/python3.6/dist-packages/carputils/resources/petsc_options/ilu_cg_opts"
    cmd+=" -ellip_options_file /usr/local/lib/python3.6/dist-packages/carputils/resources/petsc_options/amg_cg_opts"
    cmd+=" +F carpf_laplace_LS.par -simID LR_UAC_N2"

    print(cmd)
    os.system(cmd)

    cmd=f"docker run --rm --volume={basePath}/{case}/LA/UAC_CT:/shared:z"
    cmd+=" --workdir=/shared docker.opencarp.org/opencarp/opencarp:latest"
    cmd+=" openCARP -ellip_use_pt 0 -parab_use_pt 0"
    cmd+=" -parab_options_file /usr/local/lib/python3.6/dist-packages/carputils/resources/petsc_options/ilu_cg_opts"
    cmd+=" -ellip_options_file /usr/local/lib/python3.6/dist-packages/carputils/resources/petsc_options/amg_cg_opts"
    cmd+=" +F carpf_laplace_PA.par -simID PA_UAC_N2"

    print(cmd)
    os.system(cmd)

if uac_stage2:

    print("################# UAC: Stage 2 ###################")

    cmd=f"cp /home/csi20/Projects_Local/sillett_frontiers_2024/la_strain_pipeline/param_files/*.par {basePath}/{case}/LA/UAC_CT"
    print(cmd)
    os.system(cmd)

    cmd=f"docker run --rm --volume={basePath}/{case}/LA/UAC_CT:/data cemrg/uac:latest"
    cmd+=" UAC_2A_LA"
    cmd+=" _LA_Endo"
    cmd+=" clean-Labelled-refined"
    cmd+=" 1 19 11 13 15 17 prodLaRefinedLandmarks.txt"

    print(cmd)
    os.system(cmd)

    cmd=f"docker run --rm --volume={basePath}/{case}/LA/UAC_CT:/shared:z"
    cmd+=" --workdir=/shared docker.opencarp.org/opencarp/opencarp:latest"
    cmd+=" openCARP -ellip_use_pt 0 -parab_use_pt 0"
    cmd+=" -parab_options_file /usr/local/lib/python3.6/dist-packages/carputils/resources/petsc_options/ilu_cg_opts"
    cmd+=" -ellip_options_file /usr/local/lib/python3.6/dist-packages/carputils/resources/petsc_options/amg_cg_opts"
    cmd+=" +F carpf_laplace_single_LR_P.par -simID LR_Post_UAC"

    print(cmd)
    os.system(cmd)

    cmd=f"docker run --rm --volume={basePath}/{case}/LA/UAC_CT:/shared:z"
    cmd+=" --workdir=/shared docker.opencarp.org/opencarp/opencarp:latest"
    cmd+=" openCARP -ellip_use_pt 0 -parab_use_pt 0"
    cmd+=" -parab_options_file /usr/local/lib/python3.6/dist-packages/carputils/resources/petsc_options/ilu_cg_opts"
    cmd+=" -ellip_options_file /usr/local/lib/python3.6/dist-packages/carputils/resources/petsc_options/amg_cg_opts"
    cmd+=" +F carpf_laplace_single_UD_P.par -simID UD_Post_UAC"

    print(cmd)
    os.system(cmd)

    cmd=f"docker run --rm --volume={basePath}/{case}/LA/UAC_CT:/shared:z"
    cmd+=" --workdir=/shared docker.opencarp.org/opencarp/opencarp:latest"
    cmd+=" openCARP -ellip_use_pt 0 -parab_use_pt 0"
    cmd+=" -parab_options_file /usr/local/lib/python3.6/dist-packages/carputils/resources/petsc_options/ilu_cg_opts"
    cmd+=" -ellip_options_file /usr/local/lib/python3.6/dist-packages/carputils/resources/petsc_options/amg_cg_opts"
    cmd+=" +F carpf_laplace_single_LR_A.par -simID LR_Ant_UAC"

    print(cmd)
    os.system(cmd)

    cmd=f"docker run --rm --volume={basePath}/{case}/LA/UAC_CT:/shared:z"
    cmd+=" --workdir=/shared docker.opencarp.org/opencarp/opencarp:latest"
    cmd+=" openCARP -ellip_use_pt 0 -parab_use_pt 0"
    cmd+=" -parab_options_file /usr/local/lib/python3.6/dist-packages/carputils/resources/petsc_options/ilu_cg_opts"
    cmd+=" -ellip_options_file /usr/local/lib/python3.6/dist-packages/carputils/resources/petsc_options/amg_cg_opts"
    cmd+=" +F carpf_laplace_single_UD_A.par -simID UD_Ant_UAC"

    print(cmd)
    os.system(cmd)

    cmd=f"docker run --rm --volume={basePath}/{case}/LA/UAC_CT:/data cemrg/uac:latest"
    cmd+=" UAC_2B_LA _LA_Endo clean-Labelled-refined 1 19 11 13 15 17"

    print(cmd)
    os.system(cmd)

if fibre_map:

    print("################# Fibre Mapping ###################")

    cmd=f"docker run --rm --volume={basePath}/{case}/LA/UAC_CT:/data cemrg/uac:latest"
    cmd+=" UAC_FibreMapping_Bilayer _LA_Endo _LA_Epi clean-Labelled-refined Labelled_A_6_1.lon Labelled_A_6_1.lon Fibre_A"

    print(cmd)
    os.system(cmd)

    cmd="cp Labelled_Endo.lon Labelled_Endo_avg.lon"
    print(cmd)
    os.system(cmd)
    
    cmd="cp Labelled_Epi.lon Labelled_Epi_avg.lon"
    print(cmd)
    os.system(cmd)

if generateLabelledMsh:

    print("################# Generate Labelled Mesh ###################")

    cmd=f"sudo chmod 777 {basePath}/{case}/LA/UAC_CT/Labelled_Coords_2D_Rescaling_v3_C.vtk"
    
    print(cmd)
    os.system(cmd)

    cmd=f"sudo chmod 777 {basePath}/{case}/LA/UAC_CT/clean-Labelled-refined.vtk"
    
    print(cmd)
    os.system(cmd)

    cmd=f"/home/csi20/anaconda3/envs/vtk/bin/python /home/csi20/Projects_Local/sillett_frontiers_2024/la_strain_pipeline/model_creation_scripts/py/Generate_Region_Labels_removePV.py --UAC {basePath}/{case}/LA/UAC_CT/Labelled_Coords_2D_Rescaling_v3_C.vtk --LA {basePath}/{case}/LA/UAC_CT/clean-Labelled-refined.vtk"
    # cmd=f"/home/csi20/anaconda3/envs/vtk/bin/python /home/csi20/Projects_Local/phd/Projects/Stanford/Data_Analysis/py/Generate_Region_Labels_removePV.py --UAC /home/csi20/Data/Vitaliy/{case}/LA/UAC_CT/Labelled_Coords_2D_Rescaling_v3_C.vtk --LA /home/csi20/Data/Vitaliy/{case}/LA/UAC_CT/clean-Labelled-refined-aligned.vtp"
    
    print(cmd)
    os.system(cmd)

if appendFibres:

    print("################# Append Fibres to Mesh ###################")

    cmd="/home/csi20/anaconda3/envs/vtk/bin/python /home/csi20/Projects_Local/sillett_frontiers_2024/la_strain_pipeline/model_creation_scripts/py/append_epi_endo_fibres.py"
    cmd+=f" --msh {basePath}/{case}/LA/UAC_CT/clean-Labelled-refined.vtk"
    cmd+=f" --epi-fibres {basePath}/{case}/LA/UAC_CT/Labelled_Epi.lon"
    cmd+=f" --endo-fibres {basePath}/{case}/LA/UAC_CT/Labelled_Endo.lon"
    cmd+=f" --epi-name epi_avg"
    cmd+=f" --endo-name endo_avg"

    print(cmd)
    os.system(cmd)

if rotateSegMsh:

    print("################# Rotate segmentation.vtk Mesh to create input for align_msh.py ###################")

    cmd="/home/csi20/anaconda3/envs/vtk/bin/python /home/csi20/Projects_Local/sillett_frontiers_2024/la_strain_pipeline/model_creation_scripts/py/rotate_msh.py"
    cmd+=f" {basePath}/{case}/LA/UAC_CT_align/segmentation.vtk"

    print(cmd)
    os.system(cmd)

if alignMesh:

    print("################# Align clean-Labelled-refined.vtk Mesh to Original Mesh Location ###################")

    cmd="/home/csi20/anaconda3/envs/vtk/bin/python /home/csi20/Projects_Local/sillett_frontiers_2024/la_strain_pipeline/model_creation_scripts/py/align_msh.py"
    cmd+=f" --cLr {basePath}/{case}/LA/UAC_CT/clean-Labelled-refined.vtk"
    cmd+=f" --seg-msh {basePath}/{case}/LA/UAC_CT_align/segmentation-rot.vtk"
    cmd+=f" --og-msh {basePath}/{case}/LA/UAC_CT/LA-msh-smth.vtk"
    

    print(cmd)
    os.system(cmd)