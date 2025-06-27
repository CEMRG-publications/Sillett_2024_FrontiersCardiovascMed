#!/bin/bash

# Use this loop to transform Prodcutters made in CemrgApp with a RAI converted image to correspond to the original mesh from a RPI image

# Note: Case 05 uses Transform/build/Transform instead of Transform_RPI

# For Images which are RPI, use Transform_RPI to transform prodCutters made in CemrgApp (with RAI converted image) to align with original 
# mesh

# For Images which are RAI, use Transform

for Case in Normal-1
do
	# Path=/home/csi20local/Data/RG_CT_Cases/CT-CRT-${Case}/dcm8/IntraObs_study
	dcm0Path=/home/csi20local/Data/RG_CT_Cases/${Case}/dcm0/LA-Clip
	GTPath=/home/csi20local/Data/RG_CT_Cases/${Case}/dcm4/LA-Clip

	for pC_Num in 0 1 2 3 4
	do
		# ~/Documents/VTKScripts/Transform_RPI/build/Transform_RPI $dcm0Path/prodCutter${pC_Num}.vtk $dcm0Path/prodCutter${pC_Num}Transform.vtp\
		#  ~/Data/RG_CT_Cases/$Case/nifti/dcm-8.nii
		# ~/Documents/VTKScripts/Transform_RPI/build/Transform_RPI $GTPath/prodCutter${pC_Num}.vtk $GTPath/prodCutter${pC_Num}Transform.vtp\
		#  ~/Data/RG_CT_Cases/$Case/nifti/dcm-8.nii

		# ~/Documents/VTKScripts/Transform/build/Transform $dcm0Path/prodCutter${pC_Num}.vtk $dcm0Path/prodCutter${pC_Num}Transform.vtp
		~/Documents/VTKScripts/Transform/build/Transform $GTPath/prodCutter${pC_Num}.vtk $GTPath/prodCutter${pC_Num}Transform.vtp

		echo Transformed prodCutter $pC_Num for Case $Case
	done

	# Extra clip transform

	dcm0ExtraClipPath=/home/csi20local/Data/RG_CT_Cases/${Case}/dcm0/LA-Clip/Extra-Clip
	GTExtraClipPath=/home/csi20local/Data/RG_CT_Cases/${Case}/dcm4/LA-Clip/Extra-Clip

	for pC_Num in 0 1 2 3
	do
		# ~/Documents/VTKScripts/Transform_RPI/build/Transform_RPI $dcm0ExtraClipPath/prodCutter${pC_Num}.vtk $dcm0ExtraClipPath/prodCutter${pC_Num}Transform.vtp\
		#  ~/Data/RG_CT_Cases/$Case/nifti/dcm-8.nii
		# ~/Documents/VTKScripts/Transform_RPI/build/Transform_RPI $GTExtraClipPath/prodCutter${pC_Num}.vtk $GTExtraClipPath/prodCutter${pC_Num}Transform.vtp\
		#  ~/Data/RG_CT_Cases/$Case/nifti/dcm-8.nii

		# ~/Documents/VTKScripts/Transform/build/Transform $dcm0ExtraClipPath/prodCutter${pC_Num}.vtk $dcm0ExtraClipPath/prodCutter${pC_Num}Transform.vtp
		~/Documents/VTKScripts/Transform/build/Transform $GTExtraClipPath/prodCutter${pC_Num}.vtk $GTExtraClipPath/prodCutter${pC_Num}Transform.vtp

		echo Transformed Extra-Clip prodCutter $pC_Num for Case $Case
	done

done