#!/bin/bash

## Calculate Intra observer error for clippings

## Intra observer error for SinglePV-Distances [mm]

Case=05

GT_Path=/home/csi20local/Data/RG_CT_Cases/CT-CRT-${Case}/dcm4/LA-Clip
IntraObs_Path=/home/csi20local/Data/RG_CT_Cases/CT-CRT-${Case}/dcm4/IntraObs_study

for pC_Num in 0 1 2 3 4
do
	~/Documents/MeshSimilarityScripts/PV-PVCoMDist/build/PV-PVCoMDist $GT_Path/prodCutter${pC_Num}Transform-clean.vtp\
	 $IntraObs_Path/prodCutter${pC_Num}Transform-clean.vtp >> $IntraObs_Path/IntraObs_study_absolute_distances.txt

done