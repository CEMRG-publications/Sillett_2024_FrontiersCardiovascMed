#!/bin/bash

# Deforms ED mesh to ES

## For using TSFFD deformation field, using Vxm mesh as input and Vxm mesh as GT 

## 10 frame Manual cases

for Case in CT-CRT-16 # CT-CRT-21 CT-CRT-23 CT-CRT-24 CT-CRT-25 CT-CRT-26 CT-CRT-27 CT-CRT-28 CT-CRT-29 EBR-01
do

	GTPath=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm4/Manual
	dcm0Path=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm0/Manual
	# TrackingPath=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes-Vxm-Redo
	TrackingPath=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes-Vxm-Redo

	for i in 0.0 # SW 
	do
		for j in 4e-9 # BE 
		do

			echo Case $Case SW $i BE $j

			# for k in $(seq 1 1 9)
			# do
			# 	~/Software/CemrgApp_v2.1/bin/MLib/transform-points ${dcm0Path}/seg-Vxm-clip-RealSpace.vtu\
			# 	 ${TrackingPath}/SW-${i}-BE-${j}/transformed-${k}-clip.vtu\
			# 	  -dofin ${TrackingPath}/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -ascii -St ${k}0 -verbose 3
			# done

			echo Printing info on deformed mesh...

			# Need following two commands for ASD calculation
			~/Documents/MeshSimilarityScripts/PrintMeshCellCentres/build/PrintMeshCellCentres ${TrackingPath}/SW-${i}-BE-${j}/transformed-4-clip.vtu > $TrackingPath/SW-${i}-BE-${j}/transformed-4-clip-Cell-Centres.txt
			# ~/Documents/MeshSimilarityScripts/PrintMeshCellCentres/build/PrintMeshCellCentres ${TrackingPath}/SW-${i}-BE-${j}/transformed-4-clip-RealSpace.vtu > ${TrackingPath}/SW-${i}-BE-${j}/transformed-4-clip-RealSpace-Cell-Centres.txt

			~/Documents/MeshSimilarityScripts/PrintNormalIntersections/build/PrintNormalIntersections ${TrackingPath}/SW-${i}-BE-${j}/transformed-4-clip.vtu  ${GTPath}/seg-Vxm-smth-RealSpace.vtu > ${TrackingPath}/SW-${i}-BE-${j}/normal-intersections-4.txt
			# ~/Documents/MeshSimilarityScripts/PrintNormalIntersections/build/PrintNormalIntersections ${TrackingPath}/SW-${i}-BE-${j}/transformed-4-clip-RealSpace.vtu  $GTPath/seg-Vxm-smth-RealSpace.vtu > $TrackingPath/SW-${i}-BE-${j}/normal-intersections-4-VxmRealSpace.txt

			# Need following command for DHD calculation
			~/Documents/MeshSimilarityScripts/PrintMeshPoints/build/PrintMeshPoints ${TrackingPath}/SW-${i}-BE-${j}/transformed-4-clip.vtu >  ${TrackingPath}/SW-${i}-BE-${j}/transformed-4-clip-Points.txt
			# ~/Documents/MeshSimilarityScripts/PrintMeshPoints/build/PrintMeshPoints ${TrackingPath}/SW-${i}-BE-${j}/transformed-4-clip-RealSpace.vtu >  ${TrackingPath}/SW-${i}-BE-${j}/transformed-4-clip-RealSpace-Points.txt

		done
	done

	# Print Mesh Vertex Points of GT mesh
	# Need for DHD calculation
	~/Documents/MeshSimilarityScripts/PrintMeshPoints/build/PrintMeshPoints $GTPath/seg-Vxm-smth-RealSpace.vtu > $GTPath/seg-Vxm-smth-RealSpace-Points.txt

done