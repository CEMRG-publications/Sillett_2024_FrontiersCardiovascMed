#!/bin/bash

# Create mesh from segmentations from Hao's network

for Case in 08 15 16
do
	echo CT-CRT-${Case}
	cd /media/csi20local/Seagate\ Portable\ Drive/Master/Data/RG_CT_Cases/CT-CRT-${Case}/dcm0/Hao-Network ## do this manually?

	# dcm0Path=~/Dropbox/phd/Data/RG_CT_Cases/CT-CRT-${Case}/dcm0/Hao-Network
	dcm0Path=/media/csi20local/Seagate\ Portable\ Drive/Master/Data/RG_CT_Cases/CT-CRT-${Case}/dcm0/Hao-Network
	# dcm4Path=~/Dropbox/phd/Data/RG_CT_Cases/CT-CRT-${Case}/dcm8/Hao-Network
	segPath=~/Dropbox/phd/Data/RG_CT_Cases/CT-CRT-${Case}
	# dcm8Path=~/Data/RG_CT_Cases/CT-CRT-${Case}/dcm8/Hao-Network
	# dcm9Path=~/Data/RG_CT_Cases/CT-CRT-CT-CRT-${Case}/dcm9/Hao-Network
	nameOfSeg=LA_Hao_latest.nii # Segmentation to mesh
	nameOfMesh=seg.vtk
	nameOfSmoothedMesh=seg-smth.vtk

	## Extract surface mesh from segmentation
	~/Software/CemrgApp_v2.1/bin/MLib/extract-surface ./$nameOfSeg ./$nameOfMesh -isovalue 0.5 -blur 0 -ascii -verbose 3
	
	## Smooth
	~/Software/CemrgApp_v2.1/bin/MLib/smooth-surface ./$nameOfMesh ./$nameOfSmoothedMesh -iterations 100
	
	## Resample mesh
	# meshtool resample surfmesh -msh=$dcm0Path/$nameOfSmoothedMesh -min=0.02 -max=0.6 -outmsh=$dcm0Path/seg-smth-resample.vtu
	# # meshtool resample surfmesh -msh=$dcm8Path/$nameOfSmoothedMesh -min=0.02 -max=0.6 -outmsh=$dcm8Path/seg-smth-resample.vtu
	# meshtool resample surfmesh -msh=$dcm4Path/$nameOfSmoothedMesh -min=0.02 -max=0.6 -outmsh=$dcm4Path/seg-smth-resample.vtu

	echo "Resampled Meshes for Case " $Case

done