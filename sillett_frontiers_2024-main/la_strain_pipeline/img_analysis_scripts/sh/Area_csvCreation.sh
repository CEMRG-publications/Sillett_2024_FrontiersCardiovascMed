#!/bin/bash

# Script to create area-strains-${frame}.csv for all frames using TSFFD deformation fields

basePath=/home/csi20/Data/Stanford

# TSFFD Hyperparameters to use for LA motion tracking
SW=0.0
BE=1e-9

trackingPath=${basePath}/${Case}/MT-20f/SW-${SW}-BE-${BE}
fibresPath=${basePath}/${Case}/UAC_CT

# Print Area of initial dcm0 Mesh
/home/csi20/Projects_Local/PrintCellArea/build/PrintCellArea ${fibresPath}/clean-Labelled-refined-aligned.vtp > ${fibresPath}/clean-Labelled-refined-aligned-areas.txt

for frame in $(seq 0 1 19)
do
	echo ${trackingPath}/cLr-aligned-${frame}.vtp
	# Print Areas of tracked Mesh
	/home/csi20/Projects_Local/PrintCellArea/build/PrintCellArea ${trackingPath}/cLr-aligned-${frame}.vtp > ${trackingPath}/cLr-aligned-${frame}-areas.txt

	# Area strains wrt dcm0/Manual
	python3 /home/csi20/Dropbox/phd/Projects/LA_Tracking/iPython\ Notebooks/areastrain.py\
		--dcm0-areas ${fibresPath}/clean-Labelled-refined-aligned-areas.txt\
		--trk-areas ${trackingPath}/cLr-aligned-${frame}-areas.txt\
		--strain-frame ${frame}
	
done