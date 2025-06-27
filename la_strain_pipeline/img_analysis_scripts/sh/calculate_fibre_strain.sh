## Script to automate fibre strain calculations

trackingPath=$1
uacPath=$2
numTimes=$3

# Set fibre architecture want to measure strains with respect to (default: average fibre atlas)
fibre_arch=avg
numTimes=$((numTimes - 1))

for frame in $(seq 1 1 $numTimes)
do
	echo Frame ${frame} Fibre endo_${fibre_arch}

	/home/csi20/Projects_Local/sillett_frontiers_2024/la_strain_pipeline/img_analysis_scripts/cxx/strains/build/strains ${uacPath}/clean-Labelled-refined-aligned.vtp ${trackingPath}/cLr-aligned-${frame}.vtp endo_${fibre_arch} > ${trackingPath}/endo_${fibre_arch}-strains-t${frame}.txt

	echo Frame ${frame} Fibre epi_${fibre_arch}

	/home/csi20/Projects_Local/sillett_frontiers_2024/la_strain_pipeline/img_analysis_scripts/cxx/strains/build/strains ${uacPath}/clean-Labelled-refined-aligned.vtp ${trackingPath}/cLr-aligned-${frame}.vtp epi_${fibre_arch} > ${trackingPath}/epi_${fibre_arch}-strains-t${frame}.txt

done