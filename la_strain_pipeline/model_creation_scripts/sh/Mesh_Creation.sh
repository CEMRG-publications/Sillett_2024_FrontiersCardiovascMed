## Create LA Meshes

## Change following base path for where your LA.nii segmentation is
basePath=./Backup_April2023/Dropbox/phd/Projects/Stanford/Data/DICOM_Gated_CT

# Extract surface from segmentation using mirtk
~/Software/CemrgApp_v2.1/bin/MLib/extract-surface ${basePath}/S-0046/nifti/LA.nii ${basePath}/S-0046/nifti/LA-msh.vtk -isovalue 0.5 -blur 0 -ascii -verbose 3

# Smooth surface mesh using mirtk
~/Software/CemrgApp_v2.1/bin/MLib/smooth-surface ${basePath}/S-0046/nifti/LA-msh.vtk ${basePath}/S-0046/nifti/LA-msh-smth.vtk -iterations 100
