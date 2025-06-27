#!/bin/bash

# Prints out distance between CoM of tracked MV and gold standard reference MV at dcm4

# Distances in units of mm (Absolute Distance Error)

for Case in CT-CRT-21 CT-CRT-23 CT-CRT-24 CT-CRT-25 CT-CRT-26 CT-CRT-27 CT-CRT-28 CT-CRT-29 CT-CRT-30 CT-CRT-32 EBR-01 EBR-02
do
	TrackingPath=/home/csi20local/Data/RG_CT_Cases/$Case/MT-TDownsampled
	GTPath=/home/csi20local/Data/RG_CT_Cases/$Case/dcm8/MV-Clip

	for i in 9e-3 # SW 
	do
		for j in 4e-7 # BE 
		do

			echo Case $Case SW $i BE $j

			~/Documents/MeshSimilarityScripts/PV-PVCoMDist/build/PV-PVCoMDist $TrackingPath/SW-${i}-BE-${j}/MV-Clipper-transformed-4.vtp\
			$GTPath/MV-Clipper.vtp > $TrackingPath/SW-${i}-BE-${j}/MV-distance.txt

			# ~/Documents/MeshSimilarityScripts/PV-PVCoMDist/build/PV-PVCoMDist $TrackingPath/SW-${i}-BE-${j}/MV-Clipper-transformed-4.vtp\
			# $GTPath/MV-Clipper.vtp >> $TrackingPath/SW-${i}-BE-${j}/MV-distances.txt

		done

	done
done