#!/bin/bash

let L1_x=4*$1
let L2_x=4*$2

x_res=$1
y_res=$2
z_res=$3

echo "[ input ]"
echo "Padding value                      = -1024"
echo
echo "[ transformation ]"
echo "Transformation model               = FFD"
echo "Control point spacing in T         = 10"
echo
echo "[ optimization ]"
echo "Energy preconditioning             = 0.001"
echo "Divide data terms by initial value = No"
echo "Interpolation mode                 = Linear"
echo "Epsilon                            = -1e-7"
echo "Image (dis-)similarity measure     = NMI"
echo
echo "[ Level 1 ]"
echo "Blurring [mm]                      = 3"

# echo $(( res = 2* $(( x_res )) ))

echo "Resolution [mm]                    =" $(( res = 2* $(( x_res )) )) $(( res = 2* $(( y_res )) )) $(( res = 2* $(( z_res )) ))

echo "Minimum length of steps            = 0.01"
echo "Maximum length of steps            = 4"
echo "[ Level 2 ]"
echo "Blurring [mm]                      = 6"
echo "Resolution [mm]                    = $1 $2 $3"
echo "Minimum length of steps            = 0.01"
echo "Maximum length of steps            = 4"
echo "[ Level 3 ]"
echo "Blurring [mm]                      = 12"
echo "Resolution [mm]                    = $1 $2 $3"
echo "Minimum length of steps            = 0.01"
echo "Maximum length of steps            = 4"
echo
echo "[ Grid Search ]"
echo "Bending energy weight              = 4e-10" 
echo "Sparsity weight                    = 3e-3" 
echo
echo $x_res