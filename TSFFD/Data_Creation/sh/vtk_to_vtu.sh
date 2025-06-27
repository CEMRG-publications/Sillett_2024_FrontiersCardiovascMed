## Automate vtk_to_vtu.py

segType=Manual
# segType=Hao-Network

cohort=CT-CRT
# cohort=EBR
for case in 01 
do
	echo $cohort-$case

	python ~/Projects_Local/phd/Projects/TSFFD/Data_Creation/py/vtk_to_vtu.py\
	 --vtk-msh ~/Dropbox/phd/Data/RG_CT_Cases/${cohort}/case${case}/dcm0/${segType}/seg-smth-resample-clip-vxm-space.vtk

done