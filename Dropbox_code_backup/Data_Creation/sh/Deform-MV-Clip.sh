#!/bin/bash

# Deform MV-clipper

for Case in CT-CRT-21 CT-CRT-23 CT-CRT-24 CT-CRT-25 CT-CRT-26 CT-CRT-27 CT-CRT-28 CT-CRT-29 CT-CRT-30 CT-CRT-32 EBR-01 EBR-02
do

	TrackingPath=/home/csi20local/Data/RG_CT_Cases/$Case/MT-TDownsampled
	MVClipPath=/home/csi20local/Data/RG_CT_Cases/$Case/dcm0/MV-Clip
	
	for i in 9e-3 # SW 
	do
		for j in 4e-7 #  BE 
		do

			echo Case $Case SW $i BE $j
			
			~/Software/CemrgApp_v2.1/bin/MLib/transform-points $MVClipPath/MV-Clipper.vtp $TrackingPath/SW-${i}-BE-${j}/MV-Clipper-transformed-4.vtp\
			-dofin $TrackingPath/SW-${i}-BE-${j}/SW-${i}-BE-${j}.dof -ascii -St 40 -verbose 3

		done
	done

done