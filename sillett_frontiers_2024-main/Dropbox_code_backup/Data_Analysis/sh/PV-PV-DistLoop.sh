#!/bin/bash

# Inter PV-PV Percentage errors 

# Cases requiring pC start and stop IDs 01 05

# start_IDs=(4962 5722 5825 3851 4487 3806 4596)
# stop_IDs=(5040 5799 5907 3918 4550 3864 4668)

# start_IDs_GT=(5914 7213 6147 4338 4686 4266 4885)
# stop_IDs_GT=(5998 7294 6232 4408 4751 4322 4940)

for Case in CT-CRT-21 CT-CRT-23 CT-CRT-24 CT-CRT-25 CT-CRT-26 CT-CRT-27 CT-CRT-28 CT-CRT-29 CT-CRT-30 CT-CRT-32 EBR-01 EBR-02
do
	TrackingPath=/home/csi20local/Data/RG_CT_Cases/$Case/MT-TDownsampled
	GT_Path=/home/csi20local/Data/RG_CT_Cases/$Case/dcm8/LA-Clip

	for i in 9e-3 # SW
	do

		for j in 4e-7 # BE
		do
			echo "Case " $Case "SW " ${i} "BE " ${j}

			for pC1_Num in 0 1 2 3 4
			do
				for pC2_Num in 0 1 2 3 4
				do
					# echo "pC1 " ${pC1_Num} "pC2 " ${pC2_Num}

					Trk_dist=$(~/Documents/MeshSimilarityScripts/PV-PVCoMDist/build/PV-PVCoMDist $TrackingPath/SW-${i}-BE-${j}/prodCutter${pC1_Num}-transformed-4.vtp\
					 $TrackingPath/SW-${i}-BE-${j}/prodCutter${pC2_Num}-transformed-4.vtp)

					# Trk_dist=$(~/Documents/MeshSimilarityScripts/PV-PVCoMDist/build/PV-PVCoMDist $TrackingPath/SW-${i}-BE-${j}/prodCutter${pC1_Num}-transformed-4.vtp\
					#  ${start_IDs[$pC1_Num]} ${stop_IDs[$pC1_Num]} $TrackingPath/SW-${i}-BE-${j}/prodCutter${pC2_Num}-transformed-4.vtp ${start_IDs[$pC2_Num]} ${stop_IDs[$pC2_Num]})

					# echo "Trk_dist: " $Trk_dist

					GT_dist=$(~/Documents/MeshSimilarityScripts/PV-PVCoMDist/build/PV-PVCoMDist $GT_Path/prodCutter${pC1_Num}Transform-clean.vtp\
					 $GT_Path/prodCutter${pC2_Num}Transform-clean.vtp)

					# GT_dist=$(~/Documents/MeshSimilarityScripts/PV-PVCoMDist/build/PV-PVCoMDist ~/Data/RG_CT_Cases/$Case/dcm4/LA-Clip/prodCutter${pC1_Num}Transform.vtp\
					#  ${start_IDs_GT[$pC1_Num]} ${stop_IDs_GT[$pC1_Num]} ~/Data/RG_CT_Cases/$Case/dcm4/LA-Clip/prodCutter${pC2_Num}Transform.vtp ${start_IDs_GT[$pC2_Num]} ${stop_IDs_GT[$pC2_Num]})

					# echo "GT_dist: " $GT_dist

					awk "BEGIN {print 100*($GT_dist-$Trk_dist)/$GT_dist}" > $TrackingPath/SW-${i}-BE-${j}/pC${pC1_Num}-pC${pC2_Num}-distance.txt

					awk "BEGIN {print 100*($GT_dist-$Trk_dist)/$GT_dist}" >> $TrackingPath/SW-${i}-BE-${j}/pC-pC-distances.txt

					# bc -l <<< ($GT_dist - $Trk_dist) / $GT_dist

				done
			done

		done

	done
done