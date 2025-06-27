### Script to calculate ejection fraction of LA, LV
###
###

import argparse
import sys
import nibabel as nib
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

### Functions to calculate:
 # volume of a segmentation using image resolution
 # ejection fraction


def calc_volume(multilabel_seg):
    """
    Function to return LA and LV volume from HaoNet multilabel segmentation
    
    Usage:
        * Input: path to multilabel segmentation from HaoNet
        * Output: LA_volume, LV_volume [ml]
    """
    
    ## Read in multilabel_seg as array
    seg = nib.load(multilabel_seg)
    seg_ar = seg.get_fdata()

    ## Calculate voxel volume in multilabel_seg (same as the original nifti image)
    mat = seg.affine
    vxl_vol = np.abs(mat[0,0]*mat[1,1]*mat[2,2])
    
    ## Labels for LV BP and LA BP
    labels=[1.0, 4.0]  ## [LV_label, LA_label]
    vol=np.zeros((2,))
    for i in range(0,2):
        target_label=labels[i]

        ## Count number of voxels with target_label in multilabel_seg_ar
        n_vxls = np.count_nonzero(seg_ar==target_label)

        ## Calc volume for given label
        vol[i] = n_vxls*vxl_vol

    ## Convert to ml
    vol = vol * 1e-3

    ## Check multilabel labels for LA and LV
    LA_vol = vol[1]
    LV_vol = vol[0]

    return LA_vol, LV_vol

def calc_volume_Manual(multilabel_seg):
    """
    Function to return segmentation volume from a given segmentation with label=1.0
    
    Usage:
        * Input: path to segmentation
        * Output: volume [ml]
    """
    
    ## Read in multilabel_seg as array
    seg = nib.load(multilabel_seg)
    seg_ar = seg.get_fdata()

    ## Calculate voxel volume in multilabel_seg (same as the original nifti image)
    mat = seg.affine
    vxl_vol = np.abs(mat[0,0]*mat[1,1]*mat[2,2])
    
    ## Labels for LV BP and LA BP
    labels=[1.0]  ## Only label
    vol=np.zeros((1,))
    for i in range(0,1):
        target_label=labels[i]

        ## Count number of voxels with target_label in multilabel_seg_ar
        n_vxls = np.count_nonzero(seg_ar==target_label)

        ## Calc volume for given label
        vol[i] = n_vxls*vxl_vol

    ## Convert to ml
    vol = vol * 1e-3

    return vol[0]

def calc_EF(multilabel_seg, save_volume=False, save_ef=False, nFrames=10):
    """
    Function to calculate the ejection fraction from list of volumes (will likely be 10).
    
    Usage:
        * vol_ar: array of volumes over time frames. Length should be either 10 or 20.
        
    Output:
        * LA EF, LV EF
    """
    ## Extract directory
    seg_pl = Path(multilabel_seg)

    ## First calculate volumes for all time frames
    # nFrames=10
    la_vols = np.zeros((nFrames,))
    lv_vols = np.zeros((nFrames,))

    for i in range(0, nFrames):
        print(f"Reading dcm-{i}_label_maps.nii.gz")
        la_vols[i], lv_vols[i]=calc_volume(f"{seg_pl.parent}/dcm-{i}_label_maps.nii.gz")
        print("LA volume: ", la_vols[i])

    ## Get index of largest volume in case of LA
    ## Get index of smallest volume in case of LV
    la_max = np.argmax(la_vols)
    lv_max = np.argmin(lv_vols)

    ## Calculate ejection fraction
    la_sv = la_vols[la_max] - la_vols[0]
    lv_sv = lv_vols[0] - lv_vols[lv_max]

    ## Corrected LA_emptying fraction: LA max vol - LA min vol/LA max 
    la_ef = la_sv/la_vols[la_max] * 100
    lv_ef = lv_sv/lv_vols[0] * 100

    if save_volume:
        print("Saving volumes!")
        np.savetxt(f"{seg_pl.parent.parent}/multilabel_seg_analysis/la_volumes.txt", la_vols)
        np.savetxt(f"{seg_pl.parent.parent}/multilabel_seg_analysis/lv_volumes.txt", lv_vols)

    if save_ef:
        print("Saving EF!")
        np.savetxt(f"{seg_pl.parent.parent}/multilabel_seg_analysis/LA_EF.txt", np.array([la_ef]))
        # np.savetxt(f"{seg_pl.parent.parent}/multilabel_seg_analysis/LV_EF.txt", np.array([lv_ef]))

    return la_ef, lv_ef
    
def plot_volumes(multilabel_seg, save_image=False, nFrames=10):
    """
    This script plots volume transients for both the LA and LV
    """

    ## First calculate volumes
    ## Extract directory
    seg_pl = Path(multilabel_seg)

    ## First calculate volumes for all time frames
    # nFrames=20
    la_vols = np.zeros((nFrames,))
    lv_vols = np.zeros((nFrames,))

    for i in range(0, nFrames):
        print(f"Reading dcm-{i}_label_maps.nii.gz")
        la_vols[i], lv_vols[i]=calc_volume(f"{seg_pl.parent}/dcm-{i}_label_maps.nii.gz")
        # print("LA volume: ", la_vols[i])

    ## Make plot
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    time = np.arange(0,nFrames)
    time = time/nFrames
    ax1.plot(time, la_vols)
    ax2.plot(time, lv_vols)

    ax1.set_ylabel("LA volume [ml]")
    ax2.set_ylabel("LV volume [ml]")
    ax2.set_xlabel("time (normalised)")
    
    if save_image:
        print("Saving image!")
        plt.savefig(f"{seg_pl.parent.parent}/multilabel_seg_analysis/vol_transients.png", 
                dpi=200, bbox_inches="tight")

    # plt.show()

def calc_LV_myo_volume(multilabel_seg):
    """
    Function to return LV Myo label volume from HaoNet multilabel segmentation
    
    Usage:
        * Input: path to multilabel segmentation from HaoNet
        * Output: LV_myo_volume [ml]
    """
    
    ## Read in multilabel_seg as array
    seg = nib.load(multilabel_seg)
    seg_ar = seg.get_fdata()

    ## Calculate voxel volume in multilabel_seg (same as the original nifti image)
    mat = seg.affine
    vxl_vol = np.abs(mat[0,0]*mat[1,1]*mat[2,2])
    
    ## Labels for LV MYO
    label=2.0  ## [LV_MYO_LABEL]

    ## Count number of voxels with target_label in multilabel_seg_ar
    n_vxls = np.count_nonzero(seg_ar==label)

    ## Calc volume for given label
    vol = n_vxls*vxl_vol

    ## Convert to ml
    vol = vol * 1e-3

    return vol

if __name__ == '__main__':
    
    # Path to multilabel segmentation
    path=sys.argv[1]
    
    ## Uncomment here for LAEF and LVEF calculation
    ## la, lv = calc_volume(path)
    ## print("LA volume:", la)
    ## print("LV volume:", lv)

    ## la_ef, lv_ef = calc_EF(path, save_volume=False, save_ef=True, nFrames=20)
    ## print("LA EF:", la_ef)
    ## print("LV EF:", lv_ef)

    # plot_volumes(path, save_image=False, nFrames=10)

    # vol = calc_volume_Manual(path)
    # print("Volume: ", vol)

    lv_myo_vol = calc_LV_myo_volume(path)
    print(lv_myo_vol)