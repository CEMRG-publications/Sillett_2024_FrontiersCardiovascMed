#!/bin/bash

## Register ForLoop

for Case in 31 # Cases which have 20 time frames
do
	TrackingPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/CT-CRT-${Case}/MT-HiRes-TDownsampled

	for i in 9e-2 3e-2 9e-3 3e-3 9e-4 3e-4 0.0 # SW  
	do
		for j in 4e-6 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10 # BE  
		do

			echo Case $Case SW $i BE $j

			mkdir $TrackingPath/SW-${i}-BE-${j}

			for img in $(seq 0 2 19)
			do
				cp ~/Dropbox/phd/Data/RG_CT_Cases/CT-CRT-${Case}/nifti/dcm-crop-$img.nii $TrackingPath/SW-${i}-BE-${j}/
			done

			# ~/Projects/LA_Tracking/Cfg_Files/GenerateLST_20.sh > $TrackingPath/SW-${i}-BE-${j}/imgTimes.lst
			~/Dropbox/phd/Projects/LA_Tracking/Cfg_Files/GenerateLST_20_TDownsampled.sh > $TrackingPath/SW-${i}-BE-${j}/imgTimes.lst
			~/Dropbox/phd/Projects/LA_Tracking/Cfg_Files/GenerateCFG.sh $j $i > $TrackingPath/SW-${i}-BE-${j}/Final.cfg

			~/Software/CemrgApp_v2.1/bin/MLib/register -images $TrackingPath/SW-${i}-BE-${j}/imgTimes.lst\
			 -parin $TrackingPath/SW-${i}-BE-${j}/Final.cfg\
			  -dofout $TrackingPath/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -verbose 3 -threads 30

			rm $TrackingPath/SW-${i}-BE-${j}/dcm-crop-*

		done
	done

done