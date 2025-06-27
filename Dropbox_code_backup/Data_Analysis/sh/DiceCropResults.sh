#!/bin/bash

# For loop for creating DSC errors across cases

## 10 FRAME IMGS

## Manual RPI cases
for Case in CT-CRT-31 CT-CRT-34
do

	TrackingPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes-TDownsampled
	# GT_LAClipPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm8/LA-Clip/Extra-Clip
	# NameOfGT_LAClip=PVeinsCroppedImage-RPI.nii
	dcm4path=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm8/Hao-Network

	for i in 9e-2 3e-2 9e-3 3e-3 9e-4 3e-4 0.0 # SW 
	do
		for j in 4e-6 1e-6 4e-7 1e-7 4e-8 1e-8 4e-9 1e-9 4e-10 # BE 
		do
			echo Case $Case SW $i BE $j

			echo Printing dice crop results...

			python3 ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/py/DiceCoefCrop.py\
			 --GT-seg ${dcm4path}/LA_chamber.nii\
			 --tracked-seg ${TrackingPath}/SW-${i}-BE-${j}/LA_chamber-4.nii > ${TrackingPath}/SW-${i}-BE-${j}/dice-LA_chamber.txt

			python3 ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/py/DiceCoefCrop.py\
			 --GT-seg ${dcm4path}/LA_chamber.nii\
			 --tracked-seg ${TrackingPath}/SW-${i}-BE-${j}/LA_chamber-4.nii >> ${TrackingPath}/SW-${i}-Results/dice-LA_chamber.txt

		done
	done
done

# ## Manual RAI cases
# for Case in CT-CRT-05 CT-CRT-06 CT-CRT-10
# do

# 	TrackingPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes-ImgDownsample
# 	# GT_LAClipPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm8/LA-Clip/Extra-Clip
# 	# NameOfGT_LAClip=PVeinsCroppedImage-RPI.nii
# 	dcm4path=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm4/Manual

# 	for i in 0.0 # SW 
# 	do
# 		for j in 4e-9 # BE 
# 		do
# 			echo Case $Case SW $i BE $j

# 			echo Printing dice crop results...

# 			python3 ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/py/DiceCoefCrop.py\
# 			 --GT-seg ${dcm4path}/PVeinsCroppedImage-Final-rpi-p.nii\
# 			 --tracked-seg ${TrackingPath}/SW-${i}-BE-${j}/PVeinsCroppedImage-4.nii > $TrackingPath/SW-${i}-BE-${j}/dice-PVeinsCropped.txt

# 			python3 ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/py/DiceCoefCrop.py\
# 			 --GT-seg ${dcm4path}/PVeinsCroppedImage-Final-rpi-p.nii\
# 			 --tracked-seg ${TrackingPath}/SW-${i}-BE-${j}/PVeinsCroppedImage-4.nii >> $TrackingPath/SW-${i}-Results/dice-PVeinsCropped.txt

# 		done
# 	done
# done

# ## HaoNet cases
# for Case in CT-CRT-14 #CT-CRT-17 CT-CRT-18
# do

# 	TrackingPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes-ImgDownsample
# 	# GT_LAClipPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm8/LA-Clip/Extra-Clip
# 	# NameOfGT_LAClip=PVeinsCroppedImage-RPI.nii
# 	dcm4path=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm4/Hao-Network

# 	for i in 0.0 # SW 
# 	do
# 		for j in 4e-9 # BE 
# 		do
# 			echo Case $Case SW $i BE $j

# 			echo Printing dice crop results...

# 			python3 ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/py/DiceCoefCrop.py\
# 			 --GT-seg ${dcm4path}/PVeinsCroppedImage-Final-p.nii\
# 			 --tracked-seg ${TrackingPath}/SW-${i}-BE-${j}/PVeinsCroppedImage-4.nii > $TrackingPath/SW-${i}-BE-${j}/dice-PVeinsCropped.txt

# 			python3 ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/py/DiceCoefCrop.py\
# 			 --GT-seg ${dcm4path}/PVeinsCroppedImage-Final-p.nii\
# 			 --tracked-seg ${TrackingPath}/SW-${i}-BE-${j}/PVeinsCroppedImage-4.nii >> $TrackingPath/SW-${i}-Results/dice-PVeinsCropped.txt

# 		done
# 	done
# done

# 20 FRAME IMGs

# ## HaoNet RPI cases
# for Case in CT-CRT-23 CT-CRT-24 CT-CRT-25 CT-CRT-26 CT-CRT-27 CT-CRT-29
# do

# 	TrackingPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes-ImgDownsample
# 	# GT_LAClipPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm8/LA-Clip/Extra-Clip
# 	# NameOfGT_LAClip=PVeinsCroppedImage-RPI.nii
# 	dcm4path=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm8/Hao-Network

# 	for i in 0.0 # SW 
# 	do
# 		for j in 4e-9 # BE 
# 		do
# 			echo Case $Case SW $i BE $j

# 			echo Printing dice crop results...

# 			python3 ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/py/DiceCoefCrop.py\
# 			 --GT-seg ${dcm4path}/PVeinsCroppedImage-Final-p.nii\
# 			 --tracked-seg ${TrackingPath}/SW-${i}-BE-${j}/PVeinsCroppedImage-4.nii > $TrackingPath/SW-${i}-BE-${j}/dice-PVeinsCropped.txt

# 			python3 ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/py/DiceCoefCrop.py\
# 			 --GT-seg ${dcm4path}/PVeinsCroppedImage-Final-p.nii\
# 			 --tracked-seg ${TrackingPath}/SW-${i}-BE-${j}/PVeinsCroppedImage-4.nii >> $TrackingPath/SW-${i}-Results/dice-PVeinsCropped.txt

# 		done
# 	done
# done

# ## HaoNet RAI cases
# for Case in CT-CRT-21 CT-CRT-28 EBR-01
# do

# 	TrackingPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes-ImgDownsample
# 	# GT_LAClipPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm8/LA-Clip/Extra-Clip
# 	# NameOfGT_LAClip=PVeinsCroppedImage-RPI.nii
# 	dcm4path=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm8/Hao-Network

# 	for i in 0.0 # SW 
# 	do
# 		for j in 4e-9 # BE 
# 		do
# 			echo Case $Case SW $i BE $j

# 			echo Printing dice crop results...

# 			python3 ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/py/DiceCoefCrop.py\
# 			 --GT-seg ${dcm4path}/PVeinsCroppedImage-Final-rpi-p.nii\
# 			 --tracked-seg ${TrackingPath}/SW-${i}-BE-${j}/PVeinsCroppedImage-4.nii > $TrackingPath/SW-${i}-BE-${j}/dice-PVeinsCropped.txt

# 			python3 ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/py/DiceCoefCrop.py\
# 			 --GT-seg ${dcm4path}/PVeinsCroppedImage-Final-rpi-p.nii\
# 			 --tracked-seg ${TrackingPath}/SW-${i}-BE-${j}/PVeinsCroppedImage-4.nii >> $TrackingPath/SW-${i}-Results/dice-PVeinsCropped.txt

# 		done
# 	done
# done

## Manual RAI cases
# for Case in CT-CRT-32 #EBR-02
# do

# 	TrackingPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes-ImgDownsample
# 	# GT_LAClipPath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm8/LA-Clip/Extra-Clip
# 	# NameOfGT_LAClip=PVeinsCroppedImage-RPI.nii
# 	dcm4path=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm8/Manual

# 	for i in 0.0 # SW 
# 	do
# 		for j in 4e-9 # BE 
# 		do
# 			echo Case $Case SW $i BE $j

# 			echo Printing dice crop results...

# 			python3 ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/py/DiceCoefCrop.py\
# 			 --GT-seg ${dcm4path}/PVeinsCroppedImage-Final-rpi-p.nii\
# 			 --tracked-seg ${TrackingPath}/SW-${i}-BE-${j}/PVeinsCroppedImage-4.nii > $TrackingPath/SW-${i}-BE-${j}/dice-PVeinsCropped.txt

# 			python3 ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/py/DiceCoefCrop.py\
# 			 --GT-seg ${dcm4path}/PVeinsCroppedImage-Final-rpi-p.nii\
# 			 --tracked-seg ${TrackingPath}/SW-${i}-BE-${j}/PVeinsCroppedImage-4.nii >> $TrackingPath/SW-${i}-Results/dice-PVeinsCropped.txt

# 		done
# 	done
# done