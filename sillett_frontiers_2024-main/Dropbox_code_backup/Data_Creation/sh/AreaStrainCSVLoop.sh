#!/bin/bash

# Script to Create Area Strain .csv files for multiple cases. 

# CaseList=(CT-CRT-02 CT-CRT-05 CT-CRT-06 CT-CRT-07 CT-CRT-08 CT-CRT-09 CT-CRT-10 CT-CRT-12 CT-CRT-15 CT-CRT-16) # 10 frame dcm0/Manual CT-CRT-01 
CaseList=(CT-CRT-14 CT-CRT-17 CT-CRT-18) # 10 frame dcm0/Hao-Network CT-CRT-19 CT-CRT-20
# CaseList=(CT-CRT-21 CT-CRT-23 CT-CRT-24 CT-CRT-25 CT-CRT-26 CT-CRT-27 CT-CRT-28 CT-CRT-29 EBR-01) # 20 frame dcm0/Hao-Network CT-CRT-30
# CaseList=(CT-CRT-32 EBR-02) # 20 frame dcm0/Manual
# CaseList=(Normal-1 Normal-3) # Normies
# CaseList=(CT-CRT-02 CT-CRT-05 CT-CRT-06 CT-CRT-07 CT-CRT-08 CT-CRT-09 CT-CRT-10 CT-CRT-12 CT-CRT-15 CT-CRT-16)

for Case in ${CaseList[@]}
do
	echo $Case

	for frame in $(seq 1 1 9)
	do
		echo ${frame}

		# Path to initial mesh (Area Strain will be calculated wrt this mesh)
		dcm0MeshPath=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm0/Hao-Network
		dcm0MeshName=seg-Vxm-clip-RealSpace

		# Path to final mesh (Area Strain will be calculated TO this mesh)
		dcm4MeshPath=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes-ImgDownsample/SW-0.0-BE-4e-9
		dcm4MeshName=transformed-${frame}-clip-RealSpace

		# Save mesh cell areas at ED and ES.
		# echo $dcm0MeshPath/$dcm0MeshName
		# echo $dcm4MeshPath/$dcm4MeshName

		# /home/csi20local/Documents/MeshSimilarityScripts/AreaStrain/build/AreaStrain ${dcm0MeshPath}/${dcm0MeshName}.vtu > ${dcm0MeshPath}/${dcm0MeshName}-areas.txt
		/home/csi20local/Documents/MeshSimilarityScripts/AreaStrain/build/AreaStrain ${dcm4MeshPath}/${dcm4MeshName}.vtu > ${dcm4MeshPath}/${dcm4MeshName}-areas.txt

		python3 /home/csi20local/Dropbox/phd/Projects/LA_Tracking/iPython\ Notebooks/areastrain.py ${dcm0MeshPath}/${dcm0MeshName}-areas.txt ${dcm4MeshPath}/${dcm4MeshName}-areas.txt ${frame}
	
	done
done