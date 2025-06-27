#!/bin/bash

## For loop to generate ASD error for each SW BE combo

## 10 frame HaoNet cases

for Case in CT-CRT-31 CT-CRT-34
do

	GT_Path=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm8/Hao-Network
	TrackingPath=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes-TDownsampled

	for i in 9e-2 3e-2 9e-3 3e-3 9e-4 3e-4 0.0 # SW 
	do
		mkdir $TrackingPath/SW-${i}-Results

		for j in 4e-6 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10 #  BE 
		do

			echo Case $Case SW $i BE $j

			echo Printing ASD results...

			python3 ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/py/NormalsDistance.py ${TrackingPath}/SW-${i}-BE-${j}/transformed-4-clip-Cell-Centres.txt\
			${TrackingPath}/SW-${i}-BE-${j}/normal-intersections-4.txt > ${TrackingPath}/SW-${i}-BE-${j}/normal-distance.txt

			python3 ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/py/NormalsDistance.py $TrackingPath/SW-${i}-BE-${j}/transformed-4-clip-Cell-Centres.txt\
			$TrackingPath/SW-${i}-BE-${j}/normal-intersections-4.txt >> $TrackingPath/SW-${i}-Results/normal-distances.txt

		done
	done
done