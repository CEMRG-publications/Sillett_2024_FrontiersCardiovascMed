#!/bin/bash

## Register ForLoop for Cases which have 20 time frames. 
## To be run on bioeng396-pc

for Case in 23 24 25 27 30 # Cases which have 20 time frames
do

	Path=/home/csi20/CT-CRT-${Case}/MT-HiRes

	for i in 9e-2 3e-2 9e-3 3e-3 9e-4 3e-4 0.0 # SW  
	do
		for j in 4e-6 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10 # BE  
		do

			echo Case $Case SW $i BE $j

			mkdir $Path/SW-${i}-BE-${j}

			cp /home/csi20/CT-CRT-${Case}/nifti/dcm-crop-* $Path/SW-${i}-BE-${j}/

			/home/csi20/Cfg_Files/GenerateLST_20.sh > $Path/SW-${i}-BE-${j}/imgTimes.lst
			/home/csi20/Cfg_Files/GenerateCFG_20.sh $j $i > $Path/SW-${i}-BE-${j}/Final.cfg

			/home/or15/MLib/mirtk-register -images $Path/SW-${i}-BE-${j}/imgTimes.lst -parin $Path/SW-${i}-BE-${j}/Final.cfg -dofout $Path/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -verbose 3 -threads 64

			rm $Path/SW-${i}-BE-${j}/dcm-crop-*

		done
	done

done