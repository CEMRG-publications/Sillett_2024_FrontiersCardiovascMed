#!/bin/bash

# Deform ED PVeinsClippedImage to ES

for Case in 01 #02 05 06 07 08 09 12 15 16 # Cases which have 10 time frames
do

	Path=/home/csi20local/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/MT-HiRes

	for i in 9e-2 3e-2 9e-3 3e-3 9e-4 3e-4 0.0 # SW 
	do
		for j in 4e-6 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10 #  BE iteration
		do

			echo Case $Case SW $i BE $j

			k=4
			
			~/Software/CemrgApp_v2.1/bin/MLib/transform-image ~/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/dcm0/LA-Clip/Extra-Clip/PVeinsCroppedImage.nii\
			$Path/SW-${i}-BE-${j}/PVeinsCroppedImage-4.nii -dofin $Path/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -St ${k}0 -invert

			echo Output: PVeinsCroppedImage-${k}.nii

		done
	done
done