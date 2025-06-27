#!/bin/bash

# This just caluclates area of triangular mesh, not area strain

for Case in 01 # Cases which have 10 time frames
do

	# Path=/home/csi20local/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/MT-HiRes
	Path=/home/csi20local/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/MT

	for i in 9e-2 3e-2 9e-3 3e-3 9e-4 3e-4 0.0 # SW 
	do
		for j in 4e-6 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10 #  BE iteration
		do

			echo BE \
			$j

			echo Printing area strain of deformed mesh...

			~/Documents/MeshSimilarityScripts/AreaStrain/build/AreaStrain $Path/SW-${i}-BE-${j}/transformed-4-clip.vtu > $Path/SW-${i}-BE-${j}/transformed-4-clip-Area-Strain.txt

			echo Printed transformed-4-clip.vtu Area Strain at:
			echo $Path/SW-${i}-BE-${j}/transformed-4-clip-Area-Strain.txt

		done
	done

	~/Documents/MeshSimilarityScripts/AreaStrain/build/AreaStrain ~/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/dcm0/seg-smth-resample-clip.vtu > ~/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/dcm0/seg-smth-resample-clip-Area-Strain.txt

	echo Printed dcm0 seg-smooth-resample-clip.vtu Area Strain at: 
	echo /home/csi20local/Data/MarinaData/CT_Charlie/CT-CRT-${Case}/dcm0/seg-smth-resample-clip-Area-Strain.txt
done