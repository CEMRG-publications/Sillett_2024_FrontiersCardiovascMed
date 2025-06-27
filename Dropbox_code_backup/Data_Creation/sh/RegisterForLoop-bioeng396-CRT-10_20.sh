#!/bin/bash

## Register ForLoop for Cases with 10 frames on bioeng396-pc using cropped images.

for Case in CT-CRT-10 CT-CRT-20 # Cases which have 10 time frames
do
	Path=/home/csi20/$Case/MT-HiRes

	for i in 9e-2 3e-2 9e-3 3e-3 9e-4 3e-4 0.0 # SW  
	do
		for j in 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10 # BE  
		do

			echo Case $Case SW $i BE $j

			mkdir $Path/SW-${i}-BE-${j}

			for img in $(seq 0 1 9)
			do
				cp /home/csi20/$Case/nifti/dcm-crop-$img.nii $Path/SW-${i}-BE-${j}/
			done

			/home/csi20/Cfg_Files/GenerateLST.sh > $Path/SW-${i}-BE-${j}/imgTimes.lst
			/home/csi20/Cfg_Files/GenerateCFG.sh $j $i > $Path/SW-${i}-BE-${j}/Final.cfg

			/home/or15/MLib/mirtk-register -images $Path/SW-${i}-BE-${j}/imgTimes.lst -parin $Path/SW-${i}-BE-${j}/Final.cfg -dofout $Path/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -verbose 3 -threads 128

			rm $Path/SW-${i}-BE-${j}/dcm-crop-*

		done
	done

done