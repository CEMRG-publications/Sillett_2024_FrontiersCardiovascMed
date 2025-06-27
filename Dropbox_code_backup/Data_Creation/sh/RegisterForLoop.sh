#!/bin/bash

## Register ForLoop

for Case in 12 14 15 16	# Cases which have 10 time frames
do

	for i in 9e-2 3e-2 9e-3 3e-3 9e-4 3e-4 0.0 # SW 
	do
		for j in 4e-6 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10 #  BE iteration
		do

			echo BE $j

			mkdir ~/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/MT/SW-${i}-BE-${j}

			cp ~/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/nifti/dcm-crop-* ~/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/MT/SW-${i}-BE-${j}/

			~/Data/CfgFiles/GenerateLST.sh > ~/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/MT/SW-${i}-BE-${j}/imgTimes.lst
			~/Data/CfgFiles/GenerateCFG.sh $j $i > ~/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/MT/SW-${i}-BE-${j}/Final.cfg

			~/Software/CemrgApp_v2.1/bin/MLib/register -images ~/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/MT/SW-${i}-BE-${j}/imgTimes.lst\
			-parin ~/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/MT/SW-${i}-BE-${j}/Final.cfg\
			-dofout ~/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/MT/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -threads 12 -verbose 3

			rm ~/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/MT/SW-${i}-BE-${j}/dcm-crop-*

		done
	done

done