#!/bin/bash

for k in $(seq 0 1 7)
do
	python3 ~/Projects/LA_Tracking/Data_Creation/CropNifti.py /home/csi20local/Data/Angela-MT-Challenge/dcm-${k}.nii\
	/home/csi20local/Data/Angela-MT-Challenge/dcm-crop-${k}.nii 170 168 0 76 54 15

done