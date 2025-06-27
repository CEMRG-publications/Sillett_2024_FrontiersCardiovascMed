##
##
## 01 02 05 06 07 08 09 10 12

for case in 21 # 07 08 09 10 12 14 15 16 17 19 20 23 24 26 27 28 29 30 31 32 34 # 02 05 06 07 08 09 10 12 14 15 16 # 04 05 06 # 32 34 35
do
    echo "############################# case${case} #################################"

    basePath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/CT-CRT/case${case}
    # basePath=/home/csi20/Dropbox/phd/Data/RG_CT_Cases/EBR/case${case}

    trackingPath=${basePath}/MT-2D/2CH
    # baseMeshName=LA-rot-2ch-smth-save.vtk
    # baseMeshName=LA-rot-2ch-smth-save-clip-save.vtk # 01
    # baseMeshName=LA-rot-2ch-smth-save-clip.vtk # 10

    # baseMeshName=LA_Resampled_large-rot-2ch-smth-save-clip.vtk
    # baseMeshName=LA-rot-2ch-smth-save.vtk

    baseMeshName=LA-2ch-clip-save.vtk

    segmentationType=Hao-Network

    for i in $(seq 0 1 9)
    do
        /home/csi20/Software/CemrgApp_v2.1/bin/MLib/transform-points ${basePath}/dcm0/$segmentationType/$baseMeshName ${trackingPath}/transformed-${i}.vtk -dofin ${trackingPath}/tsffd.dof -St ${i}0 -ascii -verbose 3
    done
done