## script to automate extract_seg.py across cases

for case in 01 02 05 06 07 08 09 10 12 14 15 16 17 18 19 20
do
	echo "Case: $case"
	path2multilabel_seg=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/CT-CRT-01/nifti/dcm-0_label_maps.nii.gz

	python ~/Dropbox/phd/Projects/RR_VT_Case/Extract_Seg.py 