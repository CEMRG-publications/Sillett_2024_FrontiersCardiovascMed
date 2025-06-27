#!/bin/bash

for Case in 01 05 06 07 08 09 12 15 16 # Cases which have 10 time frames
do

	Path=/home/csi20local/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/MT-HiRes 	# MT or MT-HiRes

	for i in 9e-2 3e-2 9e-3 3e-3 9e-4 3e-4 0.0 # SW 
	do
		mkdir $Path/SW-${i}-Results-Automate

		for j in 4e-6 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10 # BE 
		do

			echo Case $Case SW $i BE $j

			python3 ~/Data/NormalsDistance.py $Path/SW-${i}-BE-${j}/transformed-4-clip-Cell-Centres.txt\
			$Path/SW-${i}-BE-${j}/normal-intersections-4.txt > $Path/SW-${i}-BE-${j}/normal-distance.txt

			python3 ~/Data/NormalsDistance.py $Path/SW-${i}-BE-${j}/transformed-4-clip-Cell-Centres.txt\
			$Path/SW-${i}-BE-${j}/normal-intersections-4.txt >> $Path/SW-${i}-Results-Automate/normal-distances.txt

		done
	done
done