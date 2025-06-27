## generate region labels
##

for case in EBR-01 EBR-02
do
	echo $case

	fibresPath=~/Dropbox/phd/Data/RG_CT_Cases/$case/dcm0/Fibres_HaoSeg

	python ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/py/Generate_Region_Labels_removePV.py --filepath ${fibresPath}
	# python ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/py/Generate_Region_Labels.py --filepath ${fibresPath}
done