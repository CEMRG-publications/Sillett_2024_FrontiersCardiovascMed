#!/bin/bash

## For loop to generate Hausdorff distance results

for Case in CT-CRT-31 CT-CRT-34
do

	# dcm9Path=/home/csi20local/Data/RG_CT_Cases/${Case}/dcm9/Hao-Network
	# dcm8Path=/home/csi20local/Data/RG_CT_Cases/${Case}/dcm8/Hao-Network
	GT_Path=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm8/Hao-Network
	TrackingPath=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes-TDownsampled

	for i in 9e-2 3e-2 9e-3 3e-3 9e-4 3e-4 0.0 # SW 
	do

		for j in 4e-6 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10 # BE 
		do

			echo Case $Case SW $i BE $j

			python3 ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/py/HausdorffDistance.py\
			 --tracked-vertices ${TrackingPath}/SW-${i}-BE-${j}/transformed-4-clip-Points.txt\
			  --GT-vertices ${GT_Path}/seg-smth-resample-Points.txt > ${TrackingPath}/SW-${i}-BE-${j}/hausdorff-distance.txt

			# python3 ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/HausdorffDistance.py $TrackingPath/SW-${i}-BE-${j}/transformed-4-clip-Points.txt\
			# $GT_Path/seg-smth-resample-Points.txt >> $TrackingPath/SW-${i}-Results-Automate/hausdorff-distances.txt

			python3 ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/py/HausdorffDistance.py\
			 --tracked-vertices ${TrackingPath}/SW-${i}-BE-${j}/transformed-4-clip-Points.txt\
			  --GT-vertices ${GT_Path}/seg-smth-resample-Points.txt >> ${TrackingPath}/SW-${i}-Results/hausdorff-distances.txt

		done
	done
done