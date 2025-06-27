## Automate ejection fraction.py

for case in 01 02 05 06 07 08 09 12 14 15 16 17 18 19 20
do
	echo "####### Case $case #######"
	python ejection_fraction.py /media/csi20local/Seagate\ Portable\ Drive/Master/Data/RG_CT_Cases/CT-CRT-${case}/nifti/dcm-1_label_maps.nii.gz
done