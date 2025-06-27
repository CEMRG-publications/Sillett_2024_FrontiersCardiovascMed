#!/bin/bash

## New for overall automation
## As part of StrainsMaster.sh pipeline
# Case=$1
# echo "Case: $Case"

fibresPath=$1
echo "fibresPath: $fibresPath"

trackingPath=$2
echo "trackingPath: $trackingPath"

# trackingPath=~/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes
# fibresPath=~/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm0/Fibres

for i in 0.0 # SW 
do
	for j in 1e-9 # BE 
	do

		echo Case $Case SW $i BE $j

		for k in $(seq 1 1 9)
		do
			~/Software/CemrgApp_v2.1/bin/MLib/transform-points ${fibresPath}/clean-Labelled-refined-fibres-aligned.vtp\
			 ${trackingPath}/SW-${i}-BE-${j}/cLr-fibres-aligned-${k}.vtp -dofin ${trackingPath}/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -ascii -St ${k}0 -verbose 3

		done

	done
done