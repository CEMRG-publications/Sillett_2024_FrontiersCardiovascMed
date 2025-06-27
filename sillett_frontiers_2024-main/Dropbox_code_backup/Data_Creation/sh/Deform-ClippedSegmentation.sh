#!/bin/bash

# Deform ED PVeinsClippedImage to ES

for Case in EBR-01
do
	TrackingPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes-TDownsampled
	LAClipPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm0/LA-Clip/Extra-Clip

	dcm0Path=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm0/Hao-Network
	for i in 0.0 # SW 
	do
		for j in 4e-9 # BE
		do
			echo Case $Case SW $i BE $j
			
			~/Software/CemrgApp_v2.1/bin/MLib/transform-image ${dcm0Path}/PVeinsCroppedImage-Final.nii\
			${TrackingPath}/SW-${i}-BE-${j}/PVeinsCroppedImage-4.nii\
			 -dofin ${TrackingPath}/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -St 40 -invert -threads 28

		done
	done
done

# for Case in CT-CRT-32 # CT-CRT-05 CT-CRT-06 CT-CRT-10 EBR-02
# do
# 	TrackingPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes-ImgDownsample
# 	LAClipPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm0/LA-Clip/Extra-Clip

# 	dcm0Path=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm0/Manual
# 	for i in 0.0 # SW 
# 	do
# 		for j in 4e-9 # BE
# 		do
# 			echo Case $Case SW $i BE $j
			
# 			~/Software/CemrgApp_v2.1/bin/MLib/transform-image ${dcm0Path}/PVeinsCroppedImage-Final-rpi-p.nii\
# 			${TrackingPath}/SW-${i}-BE-${j}/PVeinsCroppedImage-4.nii\
# 			 -dofin ${TrackingPath}/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -St 40 -invert -threads 28

# 		done
# 	done
# done

# for Case in CT-CRT-14 # CT-CRT-17 CT-CRT-18 CT-CRT-21 CT-CRT-23 CT-CRT-24 CT-CRT-25 CT-CRT-26 CT-CRT-27 CT-CRT-28 CT-CRT-29 EBR-01
# do
# 	TrackingPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes-ImgDownsample

# 	dcm0Path=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm0/Hao-Network
# 	for i in 0.0 # SW 
# 	do
# 		for j in 4e-9 # BE
# 		do
# 			echo Case $Case SW $i BE $j
			
# 			~/Software/CemrgApp_v2.1/bin/MLib/transform-image ${dcm0Path}/PVeinsCroppedImage-Final-p.nii\
# 			${TrackingPath}/SW-${i}-BE-${j}/PVeinsCroppedImage-4.nii\
# 			 -dofin ${TrackingPath}/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -St 40 -invert -threads 28

# 		done
# 	done
# done

# for Case in CT-CRT-21 CT-CRT-28 EBR-01
# do
# 	TrackingPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes-ImgDownsample

# 	dcm0Path=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm0/Hao-Network
# 	for i in 0.0 # SW 
# 	do
# 		for j in 4e-9 # BE
# 		do
# 			echo Case $Case SW $i BE $j
			
# 			~/Software/CemrgApp_v2.1/bin/MLib/transform-image ${dcm0Path}/PVeinsCroppedImage-Final-rpi-p.nii\
# 			${TrackingPath}/SW-${i}-BE-${j}/PVeinsCroppedImage-4.nii\
# 			 -dofin ${TrackingPath}/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -St 40 -invert -threads 28

# 		done
# 	done
# done