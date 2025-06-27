#!/bin/bash

cat /home/csi20/Projects_Local/phd/Projects/la_strain_pipeline/param_files/Template-HiRes.cfg

echo
echo "[ Grid Search ]"
echo "Bending energy weight              = $1" #NOTE: very high values reduce deformation, makes meshes very stiff
echo "Sparsity weight                    = $2" #NOTE: introduces wonky Z axis compression in places