##
##
##

for case in 04 05 06 # 01 02 05 06 07 08 09 10 12 14 15 16 17 18 19 20 21 23 24 25 26 27 28 29 30 31 32 34 35 # 07 08 09 10 12 14 15 16 17 18 19 20 21 23 24 25 26 27 28 29 30 31 32 34 35
do
    echo case$case

    # basePath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/CT-CRT/case${case}
    basePath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/EBR/case${case}
    # trackingPath=${basePath}/MT-2D/4CH
    trackingPath=${basePath}/MT-2D/2CH

    /home/csi20/Software/CemrgApp_v2.1/bin/MLib/register -images ${trackingPath}/imgTimes.lst -parin ${trackingPath}/Final.cfg -dofout ${trackingPath}/tsffd.dof -threads 28 -verbose 3

done
