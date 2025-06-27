#!/bin/bash

# Deform ED PVeinsClippedImage to ES

# For bioeng396-pc to speed up deformation of PVeinsCroppedImage using 128 cores.
# Cases 14 and 18 need their own script bcos they have MT-HiRes rather than MT-HiRes-TDownsampled.

for Case in 14 18 
do

	TrackingPath=/home/csi20/CT-CRT-$Case/MT-HiRes
	LAClipPath=/home/csi20/CT-CRT-$Case/dcm0
	SegName=PVeinsCroppedImage-RPI.nii

	for i in 9e-2 3e-2 9e-3 3e-3 9e-4 3e-4 0.0 # SW 
	do
		for j in 4e-6 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10 # BE
		do

			echo Case $Case SW $i BE $j
			
			/home/or15/MLib/transform-image $LAClipPath/$SegName\
			$TrackingPath/SW-${i}-BE-${j}/PVeinsCroppedImage-4.nii -dofin $TrackingPath/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -St 40 -invert -threads 120

		done
	done
done