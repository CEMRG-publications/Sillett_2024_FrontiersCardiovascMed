#!/bin/bash

# This file outlines the steps to create Normal Cells distance csv files for 10 time steps to create a movie 
# that SAN asked for on 31 Aug 2021

BE=1e-9
SW=3e-4
Case=05

Path2dcm0Mesh=/home/csi20local/Data/RG_CT_Cases/CT-CRT-$Case/dcm0/Manual
Path2TrackedMesh=/home/csi20local/Data/RG_CT_Cases/CT-CRT-$Case/MT-HiRes/SW-$SW-BE-$BE

for frame in $(seq 1 1 9)
do
	/home/csi20local/Documents/MeshSimilarityScripts/AreaStrain/build/AreaStrain $Path2dcm0Mesh/seg-smth-resample-clip.vtu > $Path2dcm0Mesh/seg-smth-resample-clip-cell-areas.txt
	/home/csi20local/Documents/MeshSimilarityScripts/AreaStrain/build/AreaStrain $Path2TrackedMesh/transformed-$frame-clip.vtu > $Path2TrackedMesh/transformed-$frame-clip-cell-areas.txt

	python3 /home/csi20local/Projects/LA_Tracking/Data_Analysis/AreaStrainMaps-csv_Creation.py $Path2dcm0Mesh/seg-smth-resample-clip-cell-areas.txt $Path2TrackedMesh/transformed-$frame-clip-cell-areas.txt $frame

done