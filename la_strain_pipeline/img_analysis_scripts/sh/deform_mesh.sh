## Use this script to deform LA meshes according to feature tracking

# Change basePath to path to data as needed
basePath=/home/csi20/Data/Stanford

# Directory where deformed meshes will be placed
trackingPath=${basePath}/${case}/MT/SW-0.0-BE-1e-9

# Directory with initial msh to deform
dcm0Path=${basePath}/${case}/UAC_CT

for frame in $(seq 0 1 9)
do
	/home/csi20/Software/CemrgApp_v2.1/bin/MLib/transform-points ${dcm0Path}/clean-Labelled-refined-aligned.vtp\
		${trackingPath}/cLr-aligned-${frame}.vtp -dofin ${trackingPath}/tsffd.dof -ascii -St ${frame}0 -verbose 3

done