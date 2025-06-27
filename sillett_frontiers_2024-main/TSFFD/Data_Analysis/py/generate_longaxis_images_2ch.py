"""
Use this script to rotate CT image to extract long axis 2 and 4 chamber views. 

Attempt to solve the 2chamber alignment issue by replacing 2 and 4 chamber normal order.
"""

import pyvista as pv
import numpy as np
import SimpleITK as sitk
from pathlib import Path
from utils import *
import matplotlib.pyplot as plt
import argparse
import os
from xml.dom.minidom import parse

def get_rotation_matrix_normal_vector(normal):
    
    """
    Get rotation angles in degrees from a normal vector
    """
    
    # Find angle to rotate around the x-axis
    ans=np.dot(np.array([1, 0, 0]), normal)
    theta_x=np.arccos(ans)
    theta_x=theta_x*180/np.pi
    
    # Find angle to rotate around the y-axis
    ans=np.dot(np.array([0, 1, 0]), normal)
    theta_y=np.arccos(ans)
    theta_y=theta_y*180/np.pi
    
    # Find angle to rotate around the z-axis
    ans=np.dot(np.array([0, 0, 1]), normal)
    theta_z=np.arccos(ans)
    theta_z=theta_z*180/np.pi
    
    return theta_x, theta_y, theta_z

# The following code is from https://github.com/rock-learning/pytransform3d/blob/7589e083a50597a75b12d745ebacaa7cc056cfbd/pytransform3d/rotations.py#L302
def matrix_from_axis_angle(a):
    """ Compute rotation matrix from axis-angle.
    This is called exponential map or Rodrigues' formula.
    Parameters
    ----------
    a : array-like, shape (4,)
        Axis of rotation and rotation angle: (x, y, z, angle)
    Returns
    -------
    R : array-like, shape (3, 3)
        Rotation matrix
    """
    ux, uy, uz, theta = a
    c = np.cos(theta)
    s = np.sin(theta)
    ci = 1.0 - c
    R = np.array([[ci * ux * ux + c,
                   ci * ux * uy - uz * s,
                   ci * ux * uz + uy * s],
                  [ci * uy * ux + uz * s,
                   ci * uy * uy + c,
                   ci * uy * uz - ux * s],
                  [ci * uz * ux - uy * s,
                   ci * uz * uy + ux * s,
                   ci * uz * uz + c],
                  ])

    # This is equivalent to
    # R = (np.eye(3) * np.cos(theta) +
    #      (1.0 - np.cos(theta)) * a[:3, np.newaxis].dot(a[np.newaxis, :3]) +
    #      cross_product_matrix(a[:3]) * np.sin(theta))

    return R


def resample(image, transform):
    """
    This function resamples (updates) an image using a specified transform
    :param image: The sitk image we are trying to transform
    :param transform: An sitk transform (ex. resizing, rotation, etc.
    :return: The transformed sitk image
    """
    reference_image = image
    interpolator = sitk.sitkLinear
    default_value = 0
    return sitk.Resample(image, reference_image, transform,
                         interpolator, default_value)

def resample_v2(image, transform, delta_x, delta_y, delta_z):
    """
    This function resamples (updates) an image using a specified transform
    :param image: The sitk image we are trying to transform
    :param transform: An sitk transform (ex. resizing, rotation, etc.
    :return: The transformed sitk image.
    
    Changed from resample() using object orientated approach to set output spatial resolution.
    """
    reference_image = image
    interpolator = sitk.sitkLinear
    default_value = 0
    
    # Define resample
    resampler=sitk.ResampleImageFilter()
    resampler.SetReferenceImage(reference_image)
    resampler.SetTransform(transform)
    resampler.SetInterpolator(interpolator)
    resampler.SetDefaultPixelValue(default_value)
    # Add spatial resolution
    resampler.SetOutputSpacing((delta_x, delta_y, delta_z))
    resampler.Execute(image)
    
    return resampler.Execute(image)

def get_center(img):
    """
    This function returns the physical center point of a 3d sitk image
    :param img: The sitk image we are trying to find the center of
    :return: The physical center point of the image
    """
    width, height, depth = img.GetSize()
    return img.TransformIndexToPhysicalPoint((int(np.ceil(width/2)),
                                              int(np.ceil(height/2)),
                                              int(np.ceil(depth/2))))


def rotation3d(image, theta_x, theta_y, theta_z, show=False):
    """
    This function rotates an image across each of the x, y, z axes by theta_x, theta_y, and theta_z degrees
    respectively
    :param image: An sitk MRI image
    :param theta_x: The amount of degrees the user wants the image rotated around the x axis
    :param theta_y: The amount of degrees the user wants the image rotated around the y axis
    :param theta_z: The amount of degrees the user wants the image rotated around the z axis
    :param show: Boolean, whether or not the user wants to see the result of the rotation
    :return: The rotated image
    """
    # Theta z rotation
    theta_z = np.deg2rad(theta_z)
    euler_transform = sitk.Euler3DTransform()
#     print(euler_transform.GetMatrix())
    image_center = get_center(image)
    image_resolution = image.GetSpacing()
    euler_transform.SetCenter(image_center)

    direction = image.GetDirection()
#     print("here:", direction)
    axis_angle = (direction[2], direction[5], direction[8], theta_z)
    np_rot_mat = matrix_from_axis_angle(axis_angle)
    euler_transform.SetMatrix(np_rot_mat.flatten().tolist())
    matrix_z = euler_transform.GetMatrix()
    # Change here to use resample_v2
    resampled_image = resample_v2(image, euler_transform, image_resolution[0], image_resolution[1],
                                 image_resolution[2])
    
    # Theta y rotation
    theta_y = np.deg2rad(theta_y)
    euler_transform = sitk.Euler3DTransform()
    image_center = get_center(resampled_image)
    image_resolution = image.GetSpacing()
    euler_transform.SetCenter(image_center)

    direction = resampled_image.GetDirection()
#     axis_angle = (direction[2], direction[5], theta_y, direction[11])
    axis_angle = (0, 1, 0, theta_y)
    np_rot_mat = matrix_from_axis_angle(axis_angle)
    euler_transform.SetMatrix(np_rot_mat.flatten().tolist())
    matrix_y = euler_transform.GetMatrix()
#     print(matrix_y)
    delta_x = image_resolution[0]/np.cos(theta_y)
    delta_z = image_resolution[2]/np.cos(theta_y)
    delta_x = np.abs(delta_x)
    delta_z = np.abs(delta_z)
    resampled_image = resample_v2(resampled_image, euler_transform, delta_x, image_resolution[1],
                                 delta_z)
    
    # Theta x rotation
    theta_x = np.deg2rad(theta_x)
    euler_transform = sitk.Euler3DTransform()
    image_center = get_center(resampled_image)
    euler_transform.SetCenter(image_center)

    direction = resampled_image.GetDirection()
#     axis_angle = (direction[2], theta_x, direction[8], direction[11])
    axis_angle = (1, 0, 0, theta_x)
    np_rot_mat = matrix_from_axis_angle(axis_angle)
    euler_transform.SetMatrix(np_rot_mat.flatten().tolist())
    matrix_x = euler_transform.GetMatrix()
    resampled_image = resample(resampled_image, euler_transform)
    
    if show:
        slice_num = int(input("Enter the index of the slice you would like to see"))
        plt.imshow(sitk.GetArrayFromImage(resampled_image)[slice_num])
        plt.show()
    return resampled_image, matrix_z, matrix_y, matrix_x

def save_rotation3d(image, theta_x, theta_y, theta_z, path2img, show=False, resolution=False):
    """
    This function calls rotation3d to apply 3D rotation to the image. Then saves the image
    as a nifti file.
    """
    
    image_pl=Path(path2img)
    
    rotated_img, matrix_z, matrix_y, matrix_x=rotation3d(image, theta_x, theta_y, theta_z, show=False)
    
    sitk.WriteImage(rotated_img, f'{image_pl.parent}/{image_pl.stem}-rot-2ch.nii')

def get_normal_from_mpsfile(mpsfile, flip):
    """
    Input:
        * mps file defining 3 landmarks in a plane
        * flip: set True

    Returns:
        * Normalised noraml vector to plane defined by mpsfile.
        * Landmark1
        * Landmark2
        * Landmark3
    """
    dom1=parse(mpsfile)
    xlist=dom1.getElementsByTagName("x")    
    ylist=dom1.getElementsByTagName("y")    
    zlist=dom1.getElementsByTagName("z")    
    
    LM1=np.zeros(3); 
    LM2=np.zeros(3); 
    LM3=np.zeros(3);

    LM1[0]=xlist[0].firstChild.data
    LM1[1]=ylist[0].firstChild.data
    LM1[2]=zlist[0].firstChild.data
    
    LM2[0]=xlist[1].firstChild.data
    LM2[1]=ylist[1].firstChild.data
    LM2[2]=zlist[1].firstChild.data
    
    LM3[0]=xlist[2].firstChild.data    
    LM3[1]=ylist[2].firstChild.data
    LM3[2]=zlist[2].firstChild.data

    # Flip x,y for LM data points if reading in transformed-X.vtk meshes 
    if flip:
        LM1[0]=-LM1[0]
        LM2[0]=-LM2[0]
        LM3[0]=-LM3[0]
        LM1[1]=-LM1[1]
        LM2[1]=-LM2[1]
        LM3[1]=-LM3[1]

    transform=np.eye(4)
    transform[0:3,3]=-LM1 # Move to first LM point as zero 
   
    # set up vectors created by landmarks
    LMa=(LM2-LM1)/np.linalg.norm(LM2-LM1)
    LMb=(LM3-LM1)/np.linalg.norm(LM3-LM1)
    # Check that the 2 vectors aren't colinear, if so - then move to next point
    tol=1e-2
    i=3
    while np.linalg.norm(LMa-LMb)<tol:
        LM3[0]=xlist[i].firstChild.data    
        LM3[1]=ylist[i].firstChild.data
        LM3[2]=zlist[i].firstChild.data
        LMb=(LM3-LM1)/np.linalg.norm(LM3-LM1)    
        i+=1
        if i>=xlist.length:
            print("Landmark file needs 3 points that define 2 vectors that are not co-linear.")
            sys.exit()
            
    LM_2=np.cross(LMa, LMb)
    LM_2=LM_2/np.linalg.norm(LM_2); # normalised vector that is perpendicular to 4ch long axis slice

    return LM_2, LM1, LM2, LM3

def get_landmarks_only(mpsfile):
    dom1=parse(mpsfile)
    xlist=dom1.getElementsByTagName("x")    
    ylist=dom1.getElementsByTagName("y")    
    zlist=dom1.getElementsByTagName("z")    
    
    LM1=np.zeros(3); 
    LM2=np.zeros(3); 
    LM3=np.zeros(3);

    LM1[0]=xlist[0].firstChild.data
    LM1[1]=ylist[0].firstChild.data
    LM1[2]=zlist[0].firstChild.data
    
    LM2[0]=xlist[1].firstChild.data
    LM2[1]=ylist[1].firstChild.data
    LM2[2]=zlist[1].firstChild.data
    
    LM3[0]=xlist[2].firstChild.data    
    LM3[1]=ylist[2].firstChild.data
    LM3[2]=zlist[2].firstChild.data

    return LM1, LM2, LM3

def rotate_vector(vector, rot_matrix):
    print("np.shape(vector)", np.shape(vector))
    print("np.transpose(vector)", np.shape(np.transpose(vector)))

    print("vector", vector)
    print("rot_matrix", rot_matrix)

    rotated_vector=np.dot(rot_matrix, vector)
    print("rotated_vector", rotated_vector)
    return rotated_vector

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Plot smooth strain and strain rate transients.')

    parser.add_argument('--ch4-mps', required=True, help='path to 4chamber_landmarks.mps')
    parser.add_argument('--ch2-mps', required=True, help='path to 2chamber_landmarks.mps')
    parser.add_argument('--path2img', required=True, help='path to image to rotate. E.g. /nifti/dcm-0.nii')
    parser.add_argument('--path2seg', required=True, help='path to segmentation to rotate. E.g. dcm0/Manual/LA.nii')
    parser.add_argument('--zslice', help='zSlice index to extract 4CH image from rotated 3D img', default=60)
    parser.add_argument('--yslice', help='ySlice index to extract 2CH image from rotated 3D img', default=60)
    parser.add_argument('--save-img', action='store_true', help='Flag for saving 4chamber images')
    parser.add_argument('--save-seg', action='store_true', help='Flag for saving 4chamber segmentaitons')

    args = parser.parse_args()

    ## Get Normal vectors that define the 4 and 2 chamber views for a given image: Automate this in future using get_contour*.py
    ## Following normals are for CRT/case01
    normal_4ch_view=np.array([-0.2066795813746844, 0.22997808336265405, -0.9509961260781377])
    normal_2ch_view=np.array([-0.70220524, -0.71170746, -0.01950127])

    # Automate
    normal_4ch_view, LM1, LM2, LM3=get_normal_from_mpsfile(args.ch4_mps, False)
    normal_2ch_view, LM1, LM2, LM3=get_normal_from_mpsfile(args.ch2_mps, False)

    print(normal_4ch_view)
    print(normal_2ch_view)

    # Take the angle that the 4chamber view normal makes wrt z-unit vector to get theta y.
    # theta_y will be used for rotation about y-axis to get to LAX views.
    tmp=get_rotation_matrix_normal_vector(normal_4ch_view)
    theta_y=tmp[2]

    # Take the angle that the 2chamber view normal makes wrt y-unit vector to get theta z.
    # theta_z will be used for rotation about z-axis to get to LAX views.
    tmp=get_rotation_matrix_normal_vector(normal_2ch_view)
    theta_z=tmp[1]

    print(theta_y)
    print(theta_z)

    if args.save_img:
        print("On Save Image Branch! Generating and saving rotated images (2D and 3D).")

        # For loop through all image frames
        for frame in range(1):
            print(f"Rotating frame {frame}")
            # Load CT image to be rotated into LAX views
            # path2img="/home/csi20local/Data/RG_CT_Cases/CT-CRT/case01/nifti/dcm-0.nii"
            # path2img=f"/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/CT-CRT/case01/nifti/dcm-{frame}.nii"
            path2img_pl=Path(args.path2img)
            path2img=f"{path2img_pl.parent}/dcm-{frame}.nii"
            path2img_pl=Path(path2img)
            # path2img_pl=Path(path2img)
            img=sitk.ReadImage(path2img)

            # Rotate image using theta_y and theta_z to get to 4CH and 2CH views
            # Visualise image option set to True
            resampled_image, matrix_z, matrix_y, matrix_x = rotation3d(img, 0, theta_z, theta_y, True)

            # Save rotated 3D image 
            # Comment out if don't want to save 3D image
            # save_rotation3d(img, 0, theta_z, theta_y, path2img)

            # Extract slice of rotated 3D image

            # Method 1: Note this leads to 2D slice being in different spatial position to original dcm-0-rot.nii
            # inputImage = sitk.ReadImage(f'{path2img_pl.parent}/{path2img_pl.stem}-rot.nii')
            # inputImage = sitk.ReadImage(f'{path2img_pl.parent}/dcm-0.nii')
            
            # Choose z-slice in rotated image to get 4CH image
            zslice = args.zslice
            zslice = int(zslice)
            
            # Define index to generate 4CH view
            size = list(resampled_image.GetSize())
            print(size)
            size[2] = 0
            index = [0, 0, zslice]
            print(index)
            
            Extractor = sitk.ExtractImageFilter()
            Extractor.SetSize(size)
            Extractor.SetIndex(index)

            # LM1, LM2, LM3 = get_landmarks_only(args.ch2_mps)
            # print(LM1)
            # print(np.reshape(matrix_x, (3,3)))
            # tmp=rotate_vector(LM1, np.reshape(matrix_z, (3,3)))
            # LM1_rot=rotate_vector(tmp, np.reshape(matrix_y, (3,3)))

            # RIP: Here lies an attempt to automate zslice value.
            # coords=resampled_image.TransformPhysicalPointToIndex((LM1_rot))
            # print("Slices LM1", coords)

            # coords=resampled_image.TransformPhysicalPointToIndex((LM2))
            # print("Slices LM2", coords)
            
            # coords=resampled_image.TransformPhysicalPointToIndex((LM3))
            # print("Slices LM3", coords)

            # Save 2D slice for 4CH image.
            # sitk.WriteImage(Extractor.Execute(resampled_image), f'{path2img_pl.parent}/{path2img_pl.stem}-4ch.nii')

            # Choose y-slice in rotated image to get 2CH image
            yslice = int(args.yslice)

            # Define index to generate 2CH view
            size = list(resampled_image.GetSize())
            print(size)
            size[1] = 0
            index = [0, yslice, 0]
            
            Extractor = sitk.ExtractImageFilter()
            Extractor.SetSize(size)
            Extractor.SetIndex(index)
            resampled_img=Extractor.Execute(resampled_image)
            img_ar=sitk.GetArrayFromImage(resampled_image)
            ans=img_ar.GetOrigin()
            print(ans)

            # Save 2D slice for 2CH image.
            # sitk.WriteImage(Extractor.Execute(resampled_image), f'{path2img_pl.parent}/{path2img_pl.stem}-2ch.nii')

    if args.save_seg:
        print("On Save Seg Branch! Generating and saving segmentations aligned with rotated image.")

        # Load segmentaiton
        # path2seg='/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/CT-CRT/case01/dcm0/Manual/LA.nii'
        path2seg=args.path2seg
        path2seg_pl=Path(path2seg)
        seg_img=sitk.ReadImage(path2seg)

        # Rotate segmentation by same rotation used for image.
        resampled_seg, matrix_z, matrix_y, matrix_x = rotation3d(seg_img, 0, theta_y, theta_z, False)
        # save_rotation3d(seg_img, 0, theta_y, theta_z, path2seg) # save 3d rotated seg

        # Extract 2D slice of rotated 3D seg for 4CH view
        # This ultimately doesn't help for Mesh Generation that aligns with 4CH image, but is a sanity check for seg.
        zslice = int(args.zslice)
        
        # Define parameters for 4CH 2D view
        size = list(resampled_seg.GetSize())
        print(size)
        size[2] = 0
        index = [0, 0, zslice]
        print(index)
        # Origin of new 2D image in 3D space is given by 2D slice coords in 3D space
        origin = resampled_seg.TransformIndexToPhysicalPoint(index)
        
        Extractor = sitk.ExtractImageFilter()
        Extractor.SetSize(size)
        Extractor.SetIndex(index)
        
        # Save 2D slice of 3D segmentation
        # Uncomment to save
        # sitk.WriteImage(Extractor.Execute(resampled_seg), f'{path2seg_pl.parent}/{path2seg_pl.stem}-4ch.nii')

        # Generate mesh from 3D segmentation that aligns with rotated Long Axis image
        cmd="/home/csi20local/Software/CemrgApp_v2.1/bin/MLib/extract-surface"
        cmd+= f" {path2seg_pl.parent}/{path2seg_pl.stem}-rot.nii {path2seg_pl.parent}/{path2seg_pl.stem}-rot-msh.vtk -isovalue 0.5 -blur 0 -ascii -verbose 3"
        print(cmd)
        # os.system(cmd)

        # Align the 3D mesh with 4CH 2D view
        # Read in the -rot mesh and translate it by the z coord of original Image Origin
        msh=pv.read(f"{path2seg_pl.parent}/{path2seg_pl.stem}-rot-msh.vtk")
        # Pyvista applies a default 180 degree rotation in x and y to meshes.
        # Apparently not now lol
        # pv_transf = np.zeros((4,4))
        # pv_transf[0, 0] = 1.0
        # pv_transf[1, 1] = -1.0
        # pv_transf[2, 2] = -1.0
        # pv_transf[3, 3] = 1.0
        # print("Transofmring mesh by pyvista default transform")
        # msh=msh.transform(pv_transf)

        # # Translate by z coord
        # origin_trans = np.zeros((4,4))
        # origin_trans[0, 0] = 1.0
        # origin_trans[1, 1] = 1.0
        # origin_trans[2, 2] = 1.0
        # origin_trans[3, 3] = 1.0
        # origin_trans[2, 3] = -origin[2]
        # print(origin_trans)
    
        # print("Transofmring mesh by Origin using negative Z-coordinate")
        # msh=msh.transform(origin_trans)

        # print("Saving mesh creation")
        # msh.save(f"{path2seg_pl.parent}/{path2seg_pl.stem}-4ch.vtk")

        # print("Convert mesh to read-able version for CemrgApp")
        # # cmd=f"python /home/csi20local/Projects_Local/phd/Projects/TSFFD/Data_Analysis/py/convert_mesh_type_single.py {path2seg_pl.parent}/{path2seg_pl.stem}-rot-msh-trans.vtk"
        # cmd=f"python /home/csi20local/Projects_Local/phd/Projects/TSFFD/Data_Analysis/py/convert_mesh_type_single.py {path2seg_pl.parent}/{path2seg_pl.stem}-4ch.vtk"
        # print(cmd)
        # os.system(cmd)

        # print("Smooth mesh")
        # cmd=f"/home/csi20local/Software/CemrgApp_v2.1/bin/MLib/smooth-surface {path2seg_pl.parent}/{path2seg_pl.stem}-4ch.vtk {path2seg_pl.parent}/{path2seg_pl.stem}-4ch-smth.vtk -iterations 100"
        # print(cmd)
        # os.system(cmd)

        # print("Convert smoothed mesh to read-able version for CemrgApp")
        # cmd=f"python /home/csi20local/Projects_Local/phd/Projects/TSFFD/Data_Analysis/py/convert_mesh_type_single.py {path2seg_pl.parent}/{path2seg_pl.stem}-4ch-smth.vtk"
        # print(cmd)
        # os.system(cmd)

        # Create aligned mesh for 2CH  view

        msh=pv.read(f"{path2seg_pl.parent}/{path2seg_pl.stem}-4ch.vtk")

        # Swap the y and z coordinates

        ar=msh.points
        points=np.copy(ar)

        points[:, 1] = ar[:, 2]
        points[:, 2] = ar[:, 1]

        msh.points=points

        msh.save(f"{path2seg_pl.parent}/{path2seg_pl.stem}-rot-msh-swap-yz.vtk")

        print("Convert mesh to read-able version for CemrgApp")
        cmd=f"python /home/csi20/Projects_Local/phd/Projects/TSFFD/Data_Analysis/py/convert_mesh_type_single.py {path2seg_pl.parent}/{path2seg_pl.stem}-rot-msh-swap-yz.vtk"
        print(cmd)
        os.system(cmd)

        # # Translate by negative z coord in z 
        # # Translate by Y+Z origin coordinates in y
        # origin_trans = np.zeros((4,4))
        # origin_trans[0, 0] = 1.0
        # origin_trans[1, 1] = 1.0
        # origin_trans[2, 2] = 1.0
        # origin_trans[3, 3] = 1.0
        # origin_trans[1, 3] = origin[1]+origin[2]
        # origin_trans[2, 3] = 0.0
        # print(origin_trans)

        # print("Transofmring mesh by Origin using Y and Z-coordinates")
        # # msh=pv.read(f"{path2seg_pl.parent}/{path2seg_pl.stem}-rot-msh.vtk")
        # msh=msh.transform(origin_trans)

        # print("Saving mesh creation")
        # msh.save(f"{path2seg_pl.parent}/{path2seg_pl.stem}-2ch.vtk")

        # print("Convert mesh to read-able version for CemrgApp")
        # cmd=f"python /home/csi20local/Projects_Local/phd/Projects/TSFFD/Data_Analysis/py/convert_mesh_type_single.py {path2seg_pl.parent}/{path2seg_pl.stem}-2ch.vtk"
        # print(cmd)
        # os.system(cmd)

        # print("Smooth mesh")
        # cmd=f"/home/csi20local/Software/CemrgApp_v2.1/bin/MLib/smooth-surface {path2seg_pl.parent}/{path2seg_pl.stem}-2ch.vtk {path2seg_pl.parent}/{path2seg_pl.stem}-2ch-smth.vtk -iterations 100"
        # print(cmd)
        # os.system(cmd)

        # print("Convert smoothed mesh to read-able version for CemrgApp")
        # cmd=f"python /home/csi20local/Projects_Local/phd/Projects/TSFFD/Data_Analysis/py/convert_mesh_type_single.py {path2seg_pl.parent}/{path2seg_pl.stem}-2ch-smth.vtk"
        # print(cmd)
        # os.system(cmd)