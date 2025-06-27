## This script is for creating overlays of tracked meshes with images

## TSFFD mshes

# 20_frame=True

basePath=/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/EBR/case05

for i in $(seq 0 2 18)
do
    echo $i
    
    /home/csi20local/Documents/VTKScripts/OverlayV1/build/OverlayV1 ${basePath}/nifti/dcm-$i.nii ${basePath}/Vxm/cLr-f-a-vxm-m-$i-f-0-RealSpace.vtp ${basePath}/vxm-overlay-$i.png
done

for i in $(seq 0 1 9)
do
    i_double=$(( 2*i ))
    /home/csi20local/Documents/VTKScripts/OverlayV1/build/OverlayV1 ${basePath}/nifti/dcm-$i_double.nii ${basePath}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9/cLr-aligned-$i.vtp ${basePath}/tsffd-overlay-$i_double.png
done