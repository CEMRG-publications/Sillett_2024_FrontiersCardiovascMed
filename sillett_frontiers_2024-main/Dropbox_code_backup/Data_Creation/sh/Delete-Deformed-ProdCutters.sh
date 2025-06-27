#!/bin/bash

Case=16

for i in 9e-2 3e-2 9e-3 3e-3 9e-4 3e-4 0.0
do
	for j in 4e-6 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10
	do

		# rm ~/Data/RG_CT_Cases/CT-CRT-${Case}/MT/SW-${i}-BE-${j}/prodCutter${pC_Num}-transformed-4.vtp

		for pC_Num in 0 1 2 3 4
		do 
			rm ~/Data/RG_CT_Cases/CT-CRT-${Case}/MT/SW-${i}-BE-${j}/prodCutter${pC_Num}-transformed-4.vtp

			rm ~/Data/RG_CT_Cases/CT-CRT-${Case}/MT-HiRes/SW-${i}-BE-${j}/prodCutter${pC_Num}-transformed-4.vtp

		done
	done
done
