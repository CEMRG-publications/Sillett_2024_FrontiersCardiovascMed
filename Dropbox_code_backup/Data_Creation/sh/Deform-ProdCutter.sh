#!/bin/bash

# Deform prodCutters for all SW BE combinations

for Case in CT-CRT-21 CT-CRT-23 CT-CRT-24 CT-CRT-25 CT-CRT-26 CT-CRT-27 CT-CRT-28 CT-CRT-29 CT-CRT-30 CT-CRT-32 EBR-01 EBR-02
do

	TrackingPath=/home/csi20local/Data/RG_CT_Cases/$Case/MT-TDownsampled
	dcm0ClipPath=/home/csi20local/Data/RG_CT_Cases/$Case/dcm0/LA-Clip

	for CutterNum in 0 1 2 3 4
	do
	
		for i in 9e-3 # SW 
		do
			for j in 4e-7 #  BE 
			do

				echo Case $Case Cutter $CutterNum
			
				~/Software/CemrgApp_v2.1/bin/MLib/transform-points $dcm0ClipPath/prodCutter${CutterNum}Transform-clean.vtp\
				 $TrackingPath/SW-${i}-BE-${j}/prodCutter${CutterNum}-transformed-4.vtp\
				 -dofin $TrackingPath/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -ascii -St 40 -verbose 3

				# ~/Documents/MeshSimilarityScripts/PrintDiscPoints/build/PrintDiscPoints $TrackingPath/SW-${i}-BE-${j}/prodCutter${CutterNum}-transformed-4.vtp 6160 6260 > \
				# $TrackingPath/SW-${i}-BE-${j}/prodCutter${CutterNum}-transformed-4-points.txt

				# echo Printed Disc Points at $TrackingPath/SW-${i}-BE-${j}/prodCutter${CutterNum}-transformed-4-points.txt

			done
		done

	done

	# dcm0ExtraClipPath=/home/csi20local/Data/RG_CT_Cases/$Case/dcm0/LA-Clip/Extra-Clip

	# for CutterNum in 0 1 2 3
	# do
	
	# 	for i in 9e-2 3e-2 9e-3 3e-3 9e-4 3e-4 0.0 # SW 
	# 	do
	# 		for j in 4e-6 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10 #  BE 
	# 		do

	# 			echo Case $Case Cutter $CutterNum
			
	# 			~/Software/CemrgApp_v2.1/bin/MLib/transform-points $dcm0ClipPath/prodCutter${CutterNum}Transform-clean.vtp\
	# 			 $TrackingPath/SW-${i}-BE-${j}/prodCutter${CutterNum}-transformed-4.vtp\
	# 			 -dofin $TrackingPath/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -ascii -St 40 -verbose 3

	# 			# ~/Documents/MeshSimilarityScripts/PrintDiscPoints/build/PrintDiscPoints $TrackingPath/SW-${i}-BE-${j}/prodCutter${CutterNum}-transformed-4.vtp 6160 6260 > \
	# 			# $TrackingPath/SW-${i}-BE-${j}/prodCutter${CutterNum}-transformed-4-points.txt

	# 			# echo Printed Disc Points at $TrackingPath/SW-${i}-BE-${j}/prodCutter${CutterNum}-transformed-4-points.txt

	# 		done
	# 	done

	# done

done