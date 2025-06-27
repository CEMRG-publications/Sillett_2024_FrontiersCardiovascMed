#!/bin/bash

# Deforms ED mesh to ES
# Prints tracked ES mesh cell centres and vertex points
# Prints normal intersection points from ES deformed mesh to ES GT mesh
# Print ES GT mesh vertex points

# Need to transfer:
	# dcm0/seg-smth-resample-clip.vtu 
	# dcm4/seg-smth-resample.vtu

for Case in CT-CRT-14
do

	dcm0Path=/home/csi20/${Case}/dcm0
	GTPath=/home/csi20/${Case}/dcm4
	TrackingPath=/home/csi20/${Case}/MT-HiRes

	for i in 9e-2 3e-2 9e-3 3e-3 9e-4 3e-4 0.0 # SW 
	do
		for j in 4e-6 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10 # BE 
		do

			echo Case $Case SW $i BE $j

			for k in $(seq 1 1 9)
			do
				/home/or15/MLib/mirtk-transform-points $dcm0Path/seg-smth-resample-clip.vtu\
				 $TrackingPath/SW-${i}-BE-${j}/transformed-${k}-clip.vtu -dofin $TrackingPath/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -ascii -St ${k}0 -verbose 3

			done

			echo Printing info on deformed mesh...

			~/Documents/MeshSimilarityScripts/PrintMeshCellCentres/build/PrintMeshCellCentres $TrackingPath/SW-${i}-BE-${j}/transformed-4-clip.vtu > $TrackingPath/SW-${i}-BE-${j}/transformed-4-clip-Cell-Centres.txt

			~/Documents/MeshSimilarityScripts/PrintNormalIntersections/build/PrintNormalIntersections $TrackingPath/SW-${i}-BE-${j}/transformed-4-clip.vtu  $GTPath/seg-smth-resample.vtu > $TrackingPath/SW-${i}-BE-${j}/normal-intersections-4.txt

			~/Documents/MeshSimilarityScripts/PrintMeshPoints/build/PrintMeshPoints $TrackingPath/SW-${i}-BE-${j}/transformed-4-clip.vtu >  $TrackingPath/SW-${i}-BE-${j}/transformed-4-clip-Points.txt

		done
	done

	# Print Mesh Vertex Points of GT mesh

	# ~/Documents/MeshSimilarityScripts/PrintMeshPoints/build/PrintMeshPoints $GTPath/seg-smth-resample.vtu > $GTPath/seg-smth-resample-Points.txt

done