#!/bin/bash

echo "img_path: $1"

echo "x_start: $2"
echo "y_start: $3"
echo "z_start: $4"

echo "x_size: $5"
echo "y_size: $6"
echo "z_size: $7"

img_path=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/CT-CRT-31/nifti

## Run this from within /media/cs1623/One Touch
# img_path=./Backup_April2023/Dropbox/phd/Projects/Stanford/Data/DICOM_Gated_CT/S-0001
# img_path=./Backup_April2023/Dropbox/phd/Projects/Stanford/Data/DICOM_Gated_CT/S-0287/nifti
img_path=./Backup_April2023/Dropbox/phd/Projects/Stanford/Data/DICOM_Gated_CT/S-0046/nifti

# for k in $(seq 0 1 19)
# do

# 	python ~/Dropbox/phd/Projects/LA_Tracking/Data_Creation/py/CropNifti_v3.py\
# 	 ${img_path}/dcm-${k}.nii ${img_path}/dcm-crop-${k}.nii 38 48 4 138 102 59

# done

for k in $(seq 0 1 19)
do

	python /home/csi20/Dropbox/phd/Projects/LA_Tracking/Data_Creation/py/CropNifti_v3.py\
	 ${1}/dcm-${k}.nii ${1}/dcm-crop-${k}.nii ${2} ${3} ${4} ${5} ${6} ${7}

done