#!/bin/bash

# Deform ED PVeinsClippedImage to ES (for cases with img RPI orientation) for cases with 20 imgs

for Case in CT-CRT-26 CT-CRT-29
do

	TrackingPath=/home/csi20/$Case/MT-HiRes-TDownsampled
	LAClipPath=/home/csi20/$Case/dcm0
	SegName=PVeinsCroppedImage-RPI.nii

	for i in 9e-2 3e-2 9e-3 3e-3 9e-4 3e-4 0.0 # SW 
	do
		for j in 4e-6 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10 # BE
		do

			echo Case $Case SW $i BE $j
			
			/home/or15/MLib/transform-image $LAClipPath/$SegName\
			$TrackingPath/SW-${i}-BE-${j}/PVeinsCroppedImage-4.nii -dofin $TrackingPath/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -St 40 -invert -threads 128

		done
	done
done