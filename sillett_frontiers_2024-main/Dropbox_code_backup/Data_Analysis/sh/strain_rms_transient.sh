for Case in 34
do

	case=CT-CRT/case${Case}
	basePath=~/Dropbox/phd/Data/RG_CT_Cases/${case}

	echo $case

	python ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/sh/strain_rms_transient.py\
	 --motionPath ${basePath}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9\
	  --veriMotionPath ${basePath}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9/veri\
	   --UAC ${basePath}/dcm0/Fibres_HaoSeg/LCoords_2D_R_v3_C-regional_labels.vtk\
	    --strainType endo_avg\
	     --save-png --save-txt

	python ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/sh/strain_rms_transient.py\
	 --motionPath ${basePath}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9\
	  --veriMotionPath ${basePath}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9/veri\
	   --UAC ${basePath}/dcm0/Fibres_HaoSeg/LCoords_2D_R_v3_C-regional_labels.vtk\
	    --strainType area\
	    --save-png --save-txt

done