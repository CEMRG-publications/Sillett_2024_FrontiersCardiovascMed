#!/bin/bash

# Deform ED Image to ES

for Case in CT-CRT-31 CT-CRT-34
do

	TrackingPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes-TDownsampled
	# NiftiPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/nifti
	NiftiPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm0/Hao-Network

	for i in 9e-2 3e-2 9e-3 3e-3 9e-4 3e-4 0.0 # SW 
	do
		for j in 4e-6 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10 # BE
		do

			echo Case $Case SW $i BE $j
			
			/home/csi20/Software/CemrgApp_v2.1/bin/MLib/transform-image $NiftiPath/LA_chamber.nii\
			${TrackingPath}/SW-${i}-BE-${j}/LA_chamber-4.nii -dofin ${TrackingPath}/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -St 40 -invert -threads 30

		done
	done
done
