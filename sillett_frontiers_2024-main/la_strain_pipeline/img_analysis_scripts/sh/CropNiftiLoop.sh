#!/bin/bash

# Use this script to execute CropNifti python script for all CT frames.

echo "nifti path: $1"

echo "x_start: $2"
echo "y_start: $3"
echo "z_start: $4"

echo "x_size: $5"
echo "y_size: $6"
echo "z_size: $7"

## Change the following according to where your images to crop are.

for frame in $(seq 0 1 19)
do

	python /home/csi20/Projects_Local/phd/Projects/la_strain_pipeline/img_analysis_scripts/py/${path2script}/CropNifti_v3.py ${1}/dcm-${frame}.nii ${1}/dcm-crop-${frame}.nii ${2} ${3} ${4} ${5} ${6} ${7}

done