#!/bin/bash

# Create mesh from segmentations from Hao's network

basePath=~/Dropbox/phd/Data/RG_CT_Cases/EBR

for Case in 06
do

	dcm0Path=${basePath}/case${Case}/dcm0
	# dcm4Path=~/Dropbox/phd/Data/RG_CT_Cases/CT-CRT-${Case}/dcm8/Hao-Network
	# dcm8Path=~/Data/RG_CT_Cases/CT-CRT-${Case}/dcm8/Hao-Network
	# dcm9Path=~/Data/RG_CT_Cases/CT-CRT-CT-CRT-${Case}/dcm9/Hao-Network
	nameOfSeg=LA.nii
	nameOfMesh=seg.vtk
	nameOfSmoothedMesh=seg-smth.vtk

	## Extract surface mesh from segmentation
	~/Software/CemrgApp_v2.1/bin/MLib/extract-surface $dcm0Path/$nameOfSeg $dcm0Path/$nameOfMesh -isovalue 0.5 -blur 0 -ascii -verbose 3
	# ~/Software/CemrgApp_v2.1/bin/MLib/extract-surface $dcm4Path/$nameOfSeg $dcm4Path/$nameOfMesh -isovalue 0.5 -blur 0 -ascii -verbose 3
	# ~/Software/CemrgApp_v2.1/bin/MLib/extract-surface $dcm8Path/$nameOfSeg $dcm8Path/$nameOfMesh -isovalue 0.5 -blur 0 -ascii -verbose 3

	# ~/Software/CemrgApp_v2.1/bin/MLib/extract-surface $segPath/$nameOfSeg $segPath/$nameOfMesh -isovalue 0.5 -blur 0 -ascii -verbose 3

	## Smooth mesh
	# ~/Software/CemrgApp_v2.1/bin/MLib/smooth-surface $dcm4Path/$nameOfMesh $dcm4Path/$nameOfSmoothedMesh -iterations 100
	# ~/Software/CemrgApp_v2.1/bin/MLib/smooth-surface $dcm8Path/$nameOfMesh $dcm8Path/$nameOfSmoothedMesh -iterations 100
	~/Software/CemrgApp_v2.1/bin/MLib/smooth-surface $dcm0Path/$nameOfMesh $dcm0Path/$nameOfSmoothedMesh -iterations 100
	# ~/Software/CemrgApp_v2.1/bin/MLib/smooth-surface $segPath/$nameOfMesh $segPath/$nameOfSmoothedMesh -iterations 100

	## Resample mesh
	# meshtool resample surfmesh -msh=$dcm0Path/$nameOfSmoothedMesh -min=0.02 -max=0.6 -outmsh=$dcm0Path/seg-smth-resample.vtu
	# # meshtool resample surfmesh -msh=$dcm8Path/$nameOfSmoothedMesh -min=0.02 -max=0.6 -outmsh=$dcm8Path/seg-smth-resample.vtu
	# meshtool resample surfmesh -msh=$dcm4Path/$nameOfSmoothedMesh -min=0.02 -max=0.6 -outmsh=$dcm4Path/seg-smth-resample.vtu

	echo "Resampled Meshes for Case " $Case

done