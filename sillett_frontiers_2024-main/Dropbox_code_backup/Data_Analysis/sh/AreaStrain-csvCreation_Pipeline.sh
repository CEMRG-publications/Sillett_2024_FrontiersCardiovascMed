#!/bin/bash

# Script to create area-strains-${frame}.csv for all frames 
# For StrainMaster.sh pipeline

## New for overall automation
# Case=$1
# echo "Case: $Case"
fibresPath=$1
echo "fibresPath: $fibresPath"

trackingPath=$2
echo "trackingPath: $trackingPath"

# TSFFD Hyperparameters to use for motion tracking
BE=1e-9
SW=0.0

# Location of directories containing Initial and tracked meshes
# Path2dcm0Mesh=/home/csi20local/Data/RG_CT_Cases/CT-CRT-$Case/dcm0/Manual
# trackingPath=/home/csi20local/Data/RG_CT_Cases/CT-CRT-$Case/MT-HiRes-TDownsampled/SW-$SW-BE-$BE

# Path2dcm0Mesh=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm0/Hao-Network
# trackingPath=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes-TDownsampled/SW-${SW}-BE-${BE}
# fibresPath=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm0/Fibres

# Print Area of dcm0 Mesh
~/Projects_Local/AreaStrain/build/AreaStrain ${fibresPath}/clean-Labelled-refined-fibres-aligned.vtp > ${fibresPath}/clean-Labelled-refined-fibres-aligned-areas.txt

for frame in $(seq 1 1 9)
do
	# Print Areas of tracked Mesh
	~/Projects_Local/AreaStrain/build/AreaStrain ${trackingPath}/cLr-fibres-aligned-${frame}.vtp > ${trackingPath}/cLr-fibres-aligned-${frame}-areas.txt

	# Area strains wrt dcm0/Manual
	python3 ~/Dropbox/phd/Projects/LA_Tracking/iPython\ Notebooks/areastrain.py\
	 --dcm0-areas ${fibresPath}/clean-Labelled-refined-fibres-aligned-areas.txt\
	  --trk-areas ${trackingPath}/cLr-fibres-aligned-${frame}-areas.txt\
	   --strain-frame ${frame}
	
done