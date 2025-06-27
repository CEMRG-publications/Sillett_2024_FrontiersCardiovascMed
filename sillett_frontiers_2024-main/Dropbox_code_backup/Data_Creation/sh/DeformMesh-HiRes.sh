#!/bin/bash

# Deform mesh 

# Print ES deformed mesh cell centres and vertex points
# Print normal intersection points from ES deformed mesh to ES ref mesh
# Print ES ref mesh vertex points

for Case in 31 34
do

	GTPath=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/CT-CRT-${Case}/dcm8/Hao-Network
	TrackingPath=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/CT-CRT-${Case}/MT-HiRes-TDownsampled
	dcm0Path=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/CT-CRT-${Case}/dcm0/Hao-Network
	# FibresPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/CT-CRT-${Case}/dcm0/Fibres

	# for i in 9e-2 3e-2 9e-3 3e-3 9e-4 3e-4 0.0 # SW 
	# do
	# 	for j in 4e-6 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10 # BE 
	# 	do

	# 		echo Case $Case SW $i BE $j

	# 		for k in $(seq 1 1 9)
	# 		do
	# 			~/Software/CemrgApp_v2.1/bin/MLib/transform-points ${dcm0Path}/seg-smth-resample-clip.vtu ${TrackingPath}/SW-${i}-BE-${j}/transformed-${k}-clip.vtu\
	# 			-dofin ${TrackingPath}/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -ascii -St ${k}0 -verbose 3

	# 			echo Output: transformed-${k}-clip.vtu
	# 		done

	# 		echo Printing info on deformed mesh...

	# 		## Need following two commands for ASD calculation
	# 		~/Documents/MeshSimilarityScripts/PrintMeshCellCentres/build/PrintMeshCellCentres ${TrackingPath}/SW-${i}-BE-${j}/transformed-4-clip.vtu > $TrackingPath/SW-${i}-BE-${j}/transformed-4-clip-Cell-Centres.txt

	# 		~/Documents/MeshSimilarityScripts/PrintNormalIntersections/build/PrintNormalIntersections ${TrackingPath}/SW-${i}-BE-${j}/transformed-4-clip.vtu ${GTPath}/seg-smth-resample.vtu > ${TrackingPath}/SW-${i}-BE-${j}/normal-intersections-4.txt

	# 		## Need following command for DHD calculation
	# 		~/Documents/MeshSimilarityScripts/PrintMeshPoints/build/PrintMeshPoints ${TrackingPath}/SW-${i}-BE-${j}/transformed-4-clip.vtu > ${TrackingPath}/SW-${i}-BE-${j}/transformed-4-clip-Points.txt

	# 	done
	# done

	## Need following for DHD calculation
	~/Documents/MeshSimilarityScripts/PrintMeshPoints/build/PrintMeshPoints ${GTPath}/seg-smth-resample.vtu > ${GTPath}/seg-smth-resample-Points.txt

done