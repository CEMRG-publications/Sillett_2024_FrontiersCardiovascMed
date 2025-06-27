#!/bin/bash

# Verify registration

## Modified by me 

reg_img1=false
warp_images=false
register_warp_image=false
warp_mesh=false
check_mesh_error=false

#reg_img1=true
warp_images=true
register_warp_image=true
warp_mesh=true
check_mesh_error=true

# 20f_cases="21 23 26 28 29 31"

for Case in EBR-01 # (man) ebr01 02
do
    echo "Case: $Case"

    basePath=~/Dropbox/phd/Data/RG_CT_Cases/${Case}
	motionPath=~/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9
	newMotionPath=~/Dropbox/phd/Data/RG_CT_Cases/${Case}/MT-HiRes-TDownsampled/SW-0.0-BE-1e-9/veri
    maxframes=10

    echo "Original MT dir: $motionPath"

    if [[ ! -d ${newMotionPath} ]]
    then 
        mkdir ${newMotionPath}
        
    fi
    echo "New veri MT dir: ${newMotionPath}"

    # cp /data/Dropbox/Work/Atria/GSTT/data/Final.cfg ${motionPath}/
    # cp /data/Dropbox/Work/Atria/GSTT/data/Final.cfg ${newMotionPath}/
    
    ## Register original images to create synthetic motion field 
    if ${reg_img1}
    then    
        docker run --rm --volume=${motionPath}:/data biomedia/mirtk:v1.1.0 register -images imgTimes.lst -parin Final.cfg -dofout tsffd_veri1.dof -threads 25 -verbose 3 volframes=$((${maxframes}))
    fi
    
    ## Warp original dcm0 img using synthetic motion field, to create synthetic images
    if ${warp_images}
    then    
        # cp ${motionPath}/SW-0.0-BE-1e-9.dof ${newMotionPath}/
        # cp ${motionPath}/dcm-0.nii ${newMotionPath}/
        echo "Warp images"
        for (( frame = 0; frame<$maxframes; frame++)) 
        do
            double_frame=$((2*$frame))     
            # echo "docker run --rm --volume=${newMotionPath}:/data biomedia/mirtk:v1.1.0 transform-image dcm-0.nii veri_dcm-${frame}.nii -dofin tsffd_veri1.dof -St $frame -invert -threads 12"
            # docker run --rm --volume=${newMotionPath}:/data biomedia/mirtk:v1.1.0 transform-image dcm-0.nii veri_dcm-${frame}.nii -dofin tsffd_veri1.dof -St $frame -invert -threads 12
            ~/Software/CemrgApp_v2.1/bin/MLib/transform-image ${basePath}/nifti/dcm-crop-0.nii ${motionPath}/dcm-crop-warp-${double_frame}.nii -dofin ${motionPath}/SW-0.0-BE-1e-9.dof -St ${frame}0 -invert -threads 25
        done    
    fi
    # Run image registration on warped images
    if ${register_warp_image}
    then
        cp ${motionPath}/Final.cfg ${newMotionPath}/
        cp ${motionPath}/dcm-crop-warp-*.nii ${newMotionPath}/

        cp ${motionPath}/imgTimes.lst ${newMotionPath}/imgTimes.lst
        sed -i s/'^dcm-crop'/'dcm-crop-warp'/g ${newMotionPath}/imgTimes.lst
        
        echo "Register warp images"        
        # docker run --rm --volume=${newMotionPath}:/data biomedia/mirtk:v1.1.0 register -images imgTimes2.lst -parin Final.cfg -dofout tsffd_veri2.dof -threads 12 -verbose 3
        ~/Software/CemrgApp_v2.1/bin/MLib/register -images ${newMotionPath}/imgTimes.lst -parin ${newMotionPath}/Final.cfg -dofout ${newMotionPath}/veri.dof -threads 25 -verbose 3
        
        rm ${newMotionPath}/dcm-crop-warp-*.nii
    fi
    
    # Warp mesh using veri/veri.dof
    if ${warp_mesh}
    then
        #cp ${motionPath}/transformed-*.vtk ${newMotionPath}/
        echo "Warp mesh"
        for (( frame = 0; frame<$maxframes; frame++))
        do         

            # docker run --rm --volume=${motionPath}:/data biomedia/mirtk:v1.1.0 transform-points LA0_smoothed_flip.vtk veri1_transformed-${frame}.vtk -dofin tsffd_veri1.dof -ascii -verbose 3
            # cp ${motionPath}/LA0_smoothed_flip.vtk ${newMotionPath}            
            # docker run --rm --volume=${newMotionPath}:/data biomedia/mirtk:v1.1.0 transform-points LA0_smoothed_flip.vtk veri2_transformed-${frame}.vtk -dofin tsffd_veri2.dof -ascii -verbose 3
            
            ~/Software/CemrgApp_v2.1/bin/MLib/transform-points ${basePath}/dcm0/Hao-Network/seg-smth-resample-clip.vtu ${newMotionPath}/transformed-${frame}-clip.vtu -dofin ${newMotionPath}/veri.dof -St ${frame}0 -ascii -verbose 3

        done        
    fi

    # Compare the 2 meshes 
    if ${check_mesh_error}
    then
        echo "Check mesh error"
        # for (( frame = 1; frame<$maxframes; frame++))
        # do 
        #     # python3 /data/Dropbox/Work/Atria/code/python/mesh_rms.py -mesh1 ${motionPath}/veri1_transformed-${frame}.vtk -mesh2 ${newMotionPath}/veri2_transformed-${frame}.vtk
        #     python3 ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/sh/msh_rms_cs.py --msh1 ${motionPath}/transformed-${frame}-clip.vtu --msh2 ${newMotionPath}/transformed-${frame}-clip.vtu
        # done

        python3 ~/Dropbox/phd/Projects/LA_Tracking/Data_Analysis/sh/msh_rms_transient.py --motionPath ${motionPath} --veriMotionPath ${newMotionPath} --save-png --save-txt
    fi
done
