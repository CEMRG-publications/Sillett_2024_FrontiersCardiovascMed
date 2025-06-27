#!/bin/bash

for Case in 01 02 05 06 07 08 09 12 15 16 # Cases which have 10 time frames
do

	Path=/home/csi20local/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/MT-HiRes

	for i in 9e-2 3e-2 9e-3 3e-3 9e-4 3e-4 0.0 # SW 
	do
		for j in 4e-6 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10 # BE 
		do

			echo Case $Case SW $i BE $j

			for k in $(seq 1 1 9)
			do
				~/Software/CemrgApp_v2.1/bin/MLib/transform-points ~/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/TT/input.vtk $Path/SW-${i}-BE-${j}/TT-${k}.vtk\
				-dofin $Path/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -ascii -St ${k}0 -verbose 3

				echo Output: TT-${k}.vtk

			done
		done
	done
done