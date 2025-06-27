#!/bin/bash

# Deforms ED mesh to ES
# Prints tracked ES mesh cell centres and vertex points
# Prints normal intersection points from ES deformed mesh to ES GT mesh
# Print ES GT mesh vertex points

for Case in CT-CRT-05
do

	GTPath=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm4/Manual
	dcm0Path=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm0/Hao-Network
	TrackingPath=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes-TDownsampled
	FibresPath=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm0/Fibres

	casePath=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/${Case}

	for i in 0.0 # SW 
	do
		for j in 1e-9 # BE 
		do

			echo Case $Case SW $i BE $j

			for k in $(seq 0 1 9)
			do
				~/Software/CemrgApp_v2.1/bin/MLib/transform-points ${casePath}/seg-smth.vtk\
				 ${TrackingPath}/SW-${i}-BE-${j}/LA_chamber-seg-smth-${k}.vtk -dofin ${TrackingPath}/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof\
				  -ascii -St ${k}0 -verbose 3

			done

			# ## Use below for TSFFD deformation using Downsampled images
			# for k in $(seq 1 1 9)
			# do
			# 	~/Software/CemrgApp_v2.1/bin/MLib/transform-points ${FibresPath}/clean-Labelled-refined-fibres-aligned-Vxm-space-CoM-align.vtp\
			# 	 ${TrackingPath}/SW-${i}-BE-${j}/cLr-fibres-aligned-Vxm-space-CoM-align-${k}.vtp -dofin ${TrackingPath}/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -ascii -St ${k}0 -verbose 3

			# done

			## Only need below for generating ASD/DHD mesh errors for validating tracking
			# echo Printing info on deformed mesh...

			# ## Need following two commands for ASD calculation
			# ~/Documents/MeshSimilarityScripts/PrintMeshCellCentres/build/PrintMeshCellCentres $TrackingPath/SW-${i}-BE-${j}/transformed-4-clip.vtu > $TrackingPath/SW-${i}-BE-${j}/transformed-4-clip-Cell-Centres.txt

			# ~/Documents/MeshSimilarityScripts/PrintNormalIntersections/build/PrintNormalIntersections $TrackingPath/SW-${i}-BE-${j}/transformed-4-clip.vtu  $GTPath/seg-smth-resample.vtu > $TrackingPath/SW-${i}-BE-${j}/normal-intersections-4.txt

			# ## Need following command for DHD calculation
			# ~/Documents/MeshSimilarityScripts/PrintMeshPoints/build/PrintMeshPoints $TrackingPath/SW-${i}-BE-${j}/transformed-4-clip.vtu >  $TrackingPath/SW-${i}-BE-${j}/transformed-4-clip-Points.txt

		done
	done

	# Print Mesh Vertex Points of GT mesh
	# Need for DHD calculation
	# ~/Documents/MeshSimilarityScripts/PrintMeshPoints/build/PrintMeshPoints $GTPath/seg-smth-resample.vtu > $GTPath/seg-smth-resample-Points.txt

done