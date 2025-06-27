#!/bin/bash

cat /home/csi20/Dropbox/phd/Projects/LA_Tracking/Cfg_Files/Template-HiRes.cfg

echo
echo "[ Grid Search ]"
echo "Bending energy weight              = $1" #NOTE: very high values reduce deformation, makes meshes very stiff
echo "Sparsity weight                    = $2" #NOTE: introduces wonky Z axis compression in places