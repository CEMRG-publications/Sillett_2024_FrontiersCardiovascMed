#!/bin/bash

for Case in 02 05 06 07 08 09 12 15 16 # Cases which have 10 time frames
do

	Path=/home/csi20local/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/MT-HiRes	# MT-HiRes or MT

	for i in 9e-2 3e-2 9e-3 3e-3 9e-4 3e-4 0.0 # SW 
	do
		# mkdir $Path/SW-${i}-Dice-Results

		for j in 4e-6 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10 #  BE iteration
		do

			echo Case $Case SW $i BE $j

			echo Printing dice results...

			python3 ~/Data/DiceCoef.py ~/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/dcm4/LA.nii $Path/SW-${i}-BE-${j}/LA-4.nii > $Path/SW-${i}-BE-${j}/dice.txt

			python3 ~/Data/DiceCoef.py ~/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/dcm4/LA.nii $Path/SW-${i}-BE-${j}/LA-4.nii >> $Path/SW-${i}-Results-Automate/dice.txt

		done
	done
done