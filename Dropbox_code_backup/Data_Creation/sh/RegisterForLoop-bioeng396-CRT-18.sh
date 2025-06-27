#!/bin/bash

## Register ForLoop for Case CT-CRT-18

## CT-CRT-18 requires its own Register For Loop script since it uses a different name for the cropped images 
## i.e. dcm-crop-v2-*.nii. This was because of a cropping issue with dcm-9.

for Case in 18 # Cases which have 10 time frames
do
	Path=/home/csi20/CT-CRT-18/MT-HiRes

	for i in 9e-2 3e-2 9e-3 3e-3 9e-4 3e-4 0.0 # SW  
	do
		for j in 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10 # BE  
		do

			echo Case $Case SW $i BE $j

			mkdir $Path/SW-${i}-BE-${j}

			for img in $(seq 0 1 9)
			do
				cp /home/csi20/CT-CRT-18/nifti/dcm-crop-v2-$img.nii $Path/SW-${i}-BE-${j}/
			done

			/home/csi20/Cfg_Files/GenerateLST_CRT-18.sh > $Path/SW-${i}-BE-${j}/imgTimes.lst
			/home/csi20/Cfg_Files/GenerateCFG.sh $j $i > $Path/SW-${i}-BE-${j}/Final.cfg

			/home/or15/MLib/mirtk-register -images $Path/SW-${i}-BE-${j}/imgTimes.lst -parin $Path/SW-${i}-BE-${j}/Final.cfg -dofout $Path/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -verbose 3 -threads 64

			rm $Path/SW-${i}-BE-${j}/dcm-crop-v2-*

		done
	done

done