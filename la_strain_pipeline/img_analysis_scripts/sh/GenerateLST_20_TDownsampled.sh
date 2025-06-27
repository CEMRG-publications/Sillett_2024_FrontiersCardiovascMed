#!/bin/bash
## NOTE: This generates imgTimes.lst file for cases which have 20 reconstructed CT time frames, and every other frame is being used to do the LA motion tracking (hence the first column of numbers going up in multiples of 2).
## If you are using 10 reconstructed CT time frames, you will need to change the first column of numbers to 0, 1, 2 ... 
## First col of numbers: tells the register command where to find the cropped nifti images. The second col of numbers tells you what time phase each nifti is assigned to in the register command.
echo "../../../nifti/dcm-crop- .nii"		#cropped niftis
echo "0 0"
echo "2 10"
echo "4 20"
echo "6 30"
echo "8 40"
echo "10 50"
echo "12 60"
echo "14 70"
echo "16 80"
echo "18 90"