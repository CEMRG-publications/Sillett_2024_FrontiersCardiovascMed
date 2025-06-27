### area_csvCreation generates area .txt files and area-strain .csv files

Case=$1
uacPath=$2
trackingPath=$3

echo $Case

# Print Area of dcm0 Mesh
la_strain_pipeline/img_analysis_scripts/cxx/AreaStrain/build/AreaStrain ${uacPath}/clean-Labelled-refined-aligned.vtp > ${uacPath}/clean-Labelled-refined-aligned-areas.txt

for frame in $(seq 0 1 9)
do
    echo ${trackingPath}/cLr-aligned-${frame}.vtp
    # Print Areas of tracked Mesh
    la_strain_pipeline/img_analysis_scripts/cxx/AreaStrain/build/AreaStrain ${trackingPath}/cLr-aligned-${frame}.vtp > ${trackingPath}/cLr-aligned-${frame}-areas.txt

    # Area strains wrt dcm0/Manual
    python3 /home/csi20/Projects_Local/sillett_frontiers_2024/la_strain_pipeline/img_analysis_scripts/py/areastrain.py\
        --dcm0-areas ${uacPath}/clean-Labelled-refined-aligned-areas.txt\
        --trk-areas ${trackingPath}/cLr-aligned-${frame}-areas.txt\
        --strain-frame ${frame}
    
done