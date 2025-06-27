#!/bin/bash

# Delete copied dcm- .nii

Case=01

for i in 3e-4 3e-3 0.0 9e-3 # SW 
do
	for j in 4e-6 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10 #  BE iteration
	do

		echo BE \
		$j

		rm ~/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/MT/SW-${i}-BE-${j}/dcm-*

	done
done