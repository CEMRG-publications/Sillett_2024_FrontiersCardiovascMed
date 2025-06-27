#!/bin/bash

## Register ForLoop for Res-2 

for Case in 01 02 05 06 07 08 09 12 15 16 # Cases which have 10 time frames
do
	Path=/home/csi20local/Data/RG_CT_Cases/CT-CRT-${Case}/Res-2

	for i in 3e-3 # SW  
	do
		for j in 4e-10 # BE iteration 
		do

			echo Case $Case SW $i BE $j

			mkdir $Path/SW-${i}-BE-${j}

			cp ~/Data/RG_CT_Cases/CT-CRT-${Case}/nifti/dcm-crop-* $Path/SW-${i}-BE-${j}/

			~/Projects/LA_Tracking/Cfg_Files/GenerateLST.sh > $Path/SW-${i}-BE-${j}/imgTimes.lst
			# ~/Projects/LA_Tracking/Cfg_Files/GenerateCFG.sh $j $i > ~/Data/RG_CT_Cases/CT-CRT-${Case}/MT-HiRes-3Levels-ImgRes/SW-${i}-BE-${j}/Final.cfg

			IMGRES=$(python3 ~/Projects/LA_Tracking/Cfg_Files/Get_Img_Res.py ~/Data/RG_CT_Cases/CT-CRT-${Case}/nifti/dcm-0.nii)

			python3 ~/Projects/LA_Tracking/Cfg_Files/GenerateCFG_Res2.py $IMGRES > $Path/SW-${i}-BE-${j}/Final.cfg

			~/Software/CemrgApp_v2.1/bin/MLib/register -images $Path/SW-${i}-BE-${j}/imgTimes.lst -parin $Path/SW-${i}-BE-${j}/Final.cfg -dofout $Path/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -verbose 3 -threads 12

			rm $Path/SW-${i}-BE-${j}/dcm-crop-*

		done
	done

done