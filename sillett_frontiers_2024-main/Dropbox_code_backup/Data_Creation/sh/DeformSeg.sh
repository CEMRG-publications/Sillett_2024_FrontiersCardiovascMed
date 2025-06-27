#!/bin/bash

# Deform UNCLIPPED ED segmentation to ES

for Case in 01 02 05 06 07 08 09 12 15 16 # Cases which have 10 time frames
do

	Path=/home/csi20local/Data/RG_CT_Cases/CT-CRT-${Case}/Res-1

	for i in 3e-3 # SW 
	do
		for j in 4e-10 #  BE iteration
		do

			echo Case $Case SW $i BE $j

			k=4
			
			~/Software/CemrgApp_v2.1/bin/MLib/transform-image ~/Data/RG_CT_Cases/CT-CRT-${Case}/dcm0/LA.nii\
			$Path/SW-${i}-BE-${j}/LA-4.nii -dofin $Path/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -St ${k}0 -invert -threads 12

			echo Output: LA-${k}.nii

		done
	done
done