## generate region labels
## FOr part of StrainsAnalysisMaster.sh pipeline

## Overall automation
fibresPath=$1
echo "fibresPath: $fibresPath"

# fibresPath=~/Dropbox/phd/Data/RG_CT_Cases/${Case}/dcm0/Fibres

python ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/py/Generate_Region_Labels.py --filepath ${fibresPath}