#!/bin/bash

# Deforms fibre meshes

## Original
for Case in 02 # 04 05 06 # 01 02 04 05 06 # 21 23 24 25 26 27 28 29 30 31 32 34 35
do
	# basePath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/CT-CRT/case${Case}
	basePath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/EBR/case${Case}

	trackingPath=${basePath}/MT-HiRes
	fibresPath=${basePath}/dcm0/Fibres_HaoSeg
	# fibresPath=${basePath}/dcm0/UAC_CT


	for i in 0.0 # SW 
	do
		for j in 1e-9 # BE 
		do

			echo Case $Case SW $i BE $j

			for k in $(seq 1 1 19)
			do
				# ~/Software/CemrgApp_v2.1/bin/MLib/transform-points ${fibresPath}/clean-Labelled-refined-fibres-aligned.vtp\
				#  ${trackingPath}/SW-${i}-BE-${j}/cLr-fibres-aligned-${k}.vtp -dofin ${trackingPath}/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -ascii -St ${k}0 -verbose 3

				/home/csi20/Software/CemrgApp_v2.1/bin/MLib/transform-points ${fibresPath}/clean-Labelled-refined-fibres-aligned.vtp\
				 ${trackingPath}/cLr-fibres-aligned-${k}.vtp -dofin ${trackingPath}/tsffd.dof -ascii -St ${k}0 -verbose 3

			done

		done
	done
done