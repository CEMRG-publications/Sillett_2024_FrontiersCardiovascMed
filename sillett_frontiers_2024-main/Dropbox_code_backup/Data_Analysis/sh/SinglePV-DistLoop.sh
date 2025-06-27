#!/bin/bash

# Prints out distance between CoM of tracked PVs and reference at dcm4

# Distances in units of mm
# Update: Use Cleaned prodCutters (from dcm0 and dcm4) to avoid the need for start and stop IDs lists.
# This was applied to cases: 02 06 07 08 09 12 15 16

# Cases requiring pC start and stop IDs 01 05:

# start_IDs=(4962 5722 5825 3851 4487 3806 4596)
# stop_IDs=(5040 5799 5907 3918 4550 3864 4668)

# start_IDs_GT=(5914 7213 6147 4338 4686 4266 4885)
# stop_IDs_GT=(5998 7294 6232 4408 4751 4322 4940)

for Case in CT-CRT-21 CT-CRT-23 CT-CRT-24 CT-CRT-25 CT-CRT-26 CT-CRT-27 CT-CRT-28 CT-CRT-29 CT-CRT-30 CT-CRT-32 EBR-01 EBR-02
do
	Trk_Path=/home/csi20local/Data/RG_CT_Cases/$Case/MT-TDownsampled
	GT_Path=/home/csi20local/Data/RG_CT_Cases/$Case/dcm8/LA-Clip


	for i in 9e-3 # SW iteration
	do

		for j in 4e-7 # BE iteration
		do

			echo "Case " $Case "SW " $i "BE " $j

			for pC_Num in 0 1 2 3 4
			do

				~/Documents/MeshSimilarityScripts/PV-PVCoMDist/build/PV-PVCoMDist $Trk_Path/SW-${i}-BE-${j}/prodCutter${pC_Num}-transformed-4.vtp\
				 $GT_Path/prodCutter${pC_Num}Transform-clean.vtp > $Trk_Path/SW-${i}-BE-${j}/pC${pC_Num}-distance.txt

				~/Documents/MeshSimilarityScripts/PV-PVCoMDist/build/PV-PVCoMDist $Trk_Path/SW-${i}-BE-${j}/prodCutter${pC_Num}-transformed-4.vtp\
				 $GT_Path/prodCutter${pC_Num}Transform-clean.vtp >> $Trk_Path/SW-${i}-BE-${j}/pC-distances.txt

				# ~/Documents/MeshSimilarityScripts/PV-PVCoMDist/build/PV-PVCoMDist $Trk_Path/SW-${i}-BE-${j}/prodCutter${pC_Num}-transformed-4.vtp\
				#  ${start_IDs[$pC_Num]} ${stop_IDs[$pC_Num]} $GT_Path/prodCutter${pC_Num}Transform.vtp\
				#   ${start_IDs_GT[$pC_Num]} ${stop_IDs_GT[$pC_Num]} > $Trk_Path/SW-${i}-BE-${j}/pC${pC_Num}-distance.txt

				# ~/Documents/MeshSimilarityScripts/PV-PVCoMDist/build/PV-PVCoMDist $Trk_Path/SW-${i}-BE-${j}/prodCutter${pC_Num}-transformed-4.vtp\
				#  ${start_IDs[$pC_Num]} ${stop_IDs[$pC_Num]} $GT_Path/prodCutter${pC_Num}Transform.vtp\
				#   ${start_IDs_GT[$pC_Num]} ${stop_IDs_GT[$pC_Num]} >> $Trk_Path/SW-${i}-BE-${j}/pC-distances.txt

			done

		done

	done
done