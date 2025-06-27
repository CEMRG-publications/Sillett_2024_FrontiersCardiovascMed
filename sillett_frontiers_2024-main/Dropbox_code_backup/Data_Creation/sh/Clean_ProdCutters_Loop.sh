#!/bin/bash

# Use this loop to Clean ProdCutter polydata from CemrgApp.
# This gets rid of unused points which aren't used in a cell and circumvents the need for Start and Stop Point IDs for the ProdCutter

for Case in Normal-1
do

	dcm0Path=/home/csi20local/Data/RG_CT_Cases/$Case/dcm0/LA-Clip
	GTPath=/home/csi20local/Data/RG_CT_Cases/$Case/dcm4/LA-Clip

	for pCNum in 0 1 2 3 4
	do 
		# ~/Documents/VTKScripts/CleanPolyData/build/CleanPolyData $dcm0Path/prodCutter${pCNum}Transform.vtp $dcm0Path/prodCutter${pCNum}Transform-clean.vtp
		~/Documents/VTKScripts/CleanPolyData/build/CleanPolyData $GTPath/prodCutter${pCNum}Transform.vtp $GTPath/prodCutter${pCNum}Transform-clean.vtp
		
		echo Cleaned prodCutter $pCNum for Case $Case

	done

	# For Extra-Clip ProdCutters

	dcm0ExtraClipPath=/home/csi20local/Data/RG_CT_Cases/$Case/dcm0/LA-Clip/Extra-Clip
	GTExtraClipPath=/home/csi20local/Data/RG_CT_Cases/$Case/dcm4/LA-Clip/Extra-Clip

	for pCNum in 0 1 2 3
	do 
		# ~/Documents/VTKScripts/CleanPolyData/build/CleanPolyData $dcm0ExtraClipPath/prodCutter${pCNum}Transform.vtp $dcm0ExtraClipPath/prodCutter${pCNum}Transform-clean.vtp
		~/Documents/VTKScripts/CleanPolyData/build/CleanPolyData $GTExtraClipPath/prodCutter${pCNum}Transform.vtp $GTExtraClipPath/prodCutter${pCNum}Transform-clean.vtp

		echo Cleaned prodCutter $pCNum for Case $Case
	done

done
