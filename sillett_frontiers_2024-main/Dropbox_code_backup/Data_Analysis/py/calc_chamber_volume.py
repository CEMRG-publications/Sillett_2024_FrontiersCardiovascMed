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
        # np.savetxt(f"{seg_pl.parent.parent}/multilabel_seg_analysis/LA_EF.txt", np.array([la_ef]))
        # np.savetxt(f"{seg_pl.parent.parent}/multilabel_seg_analysis/LV_EF.txt", np.array([lv_ef]))

        np.savetxt(f"{seg_pl.parent}/LA_EF.txt", np.array([la_ef]))
        np.savetxt(f"{seg_pl.parent}/LV_EF.txt", np.array([lv_ef]))

    return la_ef, lv_ef

def calc_EF_v2(multilabel_seg, save_volume=False, save_ef=False, save_image=False, nFrames=20):
    """
    v2 Function to calculate the ejection fraction from list of volumes (will likely be 10).
    
    Usage:
        * vol_ar: array of volumes over time frames. Length should be either 10 or 20.
        
    Output:
        * LA EF, LV EF

    Updates to v2:
        * Repeat the volume measurements for 2 cycle, like phasic strain results
         to better see which is min and max LA volume

        * Take min(LA volume) to be LA EDV
        * Take max(LA volume) to LA ESV

        Calculate LAEF from LA EDV and LA EDV instead of assuming 0th frame is LA EDV
    """

    ## Extract directory
    seg_pl = Path(multilabel_seg)

    ## First calculate volumes for all time frames
    # nFrames=10
    la_vols = np.zeros((nFrames,))
    lv_vols = np.zeros((nFrames,))

    # frame_list=range(nFrames)
    # frame_list=list(frame_list)
    # frame_list.remove(1)

    # frame_num = np.arange(20, 120, 10)

    for i in range(0, nFrames):
        print(f"Reading dcm-{i}_label_maps.nii.gz")
        la_vols[i], lv_vols[i]=calc_volume(f"{seg_pl.parent}/dcm-{i}_label_maps.nii.gz")
        print("LA volume: ", la_vols[i])

    ## Repeat cardiac cycle
    la_vols_list = list(la_vols)
    lv_vols_list = list(lv_vols)

    la_vols_list_repeat = la_vols_list + la_vols_list
    lv_vols_list_repeat = lv_vols_list + lv_vols_list

    ## Make plot
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    time = np.arange(0,nFrames*2)
    time = time/nFrames
    ax1.plot(time, la_vols_list_repeat)
    ax2.plot(time, lv_vols_list_repeat)

    ax1.set_ylabel("LA volume [ml]")
    ax2.set_ylabel("LV volume [ml]")
    ax2.set_xlabel("time (normalised)")

    plt.suptitle(f"{seg_pl.parent.parent.stem}")

    if save_image:
        print("Saving image!")
        plt.savefig(f"{seg_pl.parent}/la_lv_vol_transients_v2.png", 
                dpi=200, bbox_inches="tight")

    # plt.show()
    ## End plot

    ## Get index of largest volume in case of LA
    ## Get index of smallest volume in case of LV
    la_max_idx = np.argmax(la_vols)
    la_min_idx = np.argmin(la_vols)

    lv_max_idx = np.argmax(lv_vols)
    lv_min_idx = np.argmin(lv_vols)

    ## Calculate ejection fraction
    la_sv = la_vols[la_max_idx] - la_vols[la_min_idx]
    lv_sv = lv_vols[lv_max_idx] - lv_vols[lv_min_idx]

    ## Corrected LA_emptying fraction: LA max vol - LA min vol/LA max 
    la_ef = la_sv/la_vols[la_max_idx] * 100
    lv_ef = lv_sv/lv_vols[lv_max_idx] * 100

    la_edv = la_vols[la_min_idx]
    la_esv = la_vols[la_max_idx]

    lv_edv = lv_vols[lv_max_idx]
    lv_esv = lv_vols[lv_min_idx]

    if save_volume:
        print("Saving volumes!")
        np.savetxt(f"{seg_pl.parent}/la_volumes_v2.txt", la_vols,fmt="%g")
        np.savetxt(f"{seg_pl.parent}/lv_volumes_v2.txt", lv_vols,fmt="%g")

        np.savetxt(f"{seg_pl.parent}/LA_EDV_v2.txt", np.array([la_edv]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LA_ESV_v2.txt", np.array([la_esv]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LV_EDV_v2.txt", np.array([lv_edv]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LV_ESV_v2.txt", np.array([lv_esv]),fmt="%g")

    if save_ef:
        print("Saving EF!")
        # np.savetxt(f"{seg_pl.parent.parent}/multilabel_seg_analysis/LA_EF.txt", np.array([la_ef]))
        # np.savetxt(f"{seg_pl.parent.parent}/multilabel_seg_analysis/LV_EF.txt", np.array([lv_ef]))

        np.savetxt(f"{seg_pl.parent}/LA_EF_v2.txt", np.array([la_ef]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LV_EF_v2.txt", np.array([lv_ef]),fmt="%g")

    return la_ef, lv_ef

def calc_EF_v2_S400(multilabel_seg, save_volume=False, save_ef=False, save_image=False, nFrames=20):
    """
    v2 Function to calculate the ejection fraction from list of volumes (will likely be 10).
    
    Usage:
        * vol_ar: array of volumes over time frames. Length should be either 10 or 20.
        
    Output:
        * LA EF, LV EF

    Updates to v2:
        * Repeat the volume measurements for 2 cycle, like phasic strain results
         to better see which is min and max LA volume

        * Take min(LA volume) to be LA EDV
        * Take max(LA volume) to LA ESV

        Calculate LAEF from LA EDV and LA EDV instead of assuming 0th frame is LA EDV
    """

    ## Extract directory
    seg_pl = Path(multilabel_seg)

    ## First calculate volumes for all time frames
    # nFrames=10
    la_vols = np.zeros((nFrames-1,))
    lv_vols = np.zeros((nFrames-1,))

    frame_list=range(nFrames)
    frame_list=list(frame_list)
    frame_list.remove(1)

    # for i in range(0, nFrames):
    for i, frame in enumerate(frame_list):
        print(f"Reading dcm-{frame}_label_maps.nii.gz")
        la_vols[i], lv_vols[i]=calc_volume(f"{seg_pl.parent}/dcm-{frame}_label_maps.nii.gz")
        print("LA volume: ", la_vols[i])

    ## Repeat cardiac cycle
    la_vols_list = list(la_vols)
    lv_vols_list = list(lv_vols)

    la_vols_list_repeat = la_vols_list + la_vols_list
    lv_vols_list_repeat = lv_vols_list + lv_vols_list

    ## Make plot
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    time = np.arange(0,2*len(frame_list))
    time = time/nFrames
    ax1.plot(time, la_vols_list_repeat)
    ax2.plot(time, lv_vols_list_repeat)

    ax1.set_ylabel("LA volume [ml]")
    ax2.set_ylabel("LV volume [ml]")
    ax2.set_xlabel("time (normalised)")

    plt.suptitle(f"{seg_pl.parent.parent.stem}")

    if save_image:
        print("Saving image!")
        plt.savefig(f"{seg_pl.parent}/la_lv_vol_transients_v2.png", 
                dpi=200, bbox_inches="tight")

    # plt.show()
    ## End plot

    ## Get index of largest volume in case of LA
    ## Get index of smallest volume in case of LV
    la_max_idx = np.argmax(la_vols)
    la_min_idx = np.argmin(la_vols)

    lv_max_idx = np.argmax(lv_vols)
    lv_min_idx = np.argmin(lv_vols)

    ## Calculate ejection fraction
    la_sv = la_vols[la_max_idx] - la_vols[la_min_idx]
    lv_sv = lv_vols[lv_max_idx] - lv_vols[lv_min_idx]

    ## Corrected LA_emptying fraction: LA max vol - LA min vol/LA max 
    la_ef = la_sv/la_vols[la_max_idx] * 100
    lv_ef = lv_sv/lv_vols[lv_max_idx] * 100

    la_edv = la_vols[la_min_idx]
    la_esv = la_vols[la_max_idx]

    lv_edv = lv_vols[lv_max_idx]
    lv_esv = lv_vols[lv_min_idx]

    if save_volume:
        print("Saving volumes!")
        # np.savetxt(f"{seg_pl.parent}/la_volumes_v2.txt", la_vols,fmt="%g")
        # np.savetxt(f"{seg_pl.parent}/lv_volumes_v2.txt", lv_vols,fmt="%g")

        np.savetxt(f"{seg_pl.parent}/LA_EDV_v2.txt", np.array([la_edv]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LA_ESV_v2.txt", np.array([la_esv]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LV_EDV_v2.txt", np.array([lv_edv]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LV_ESV_v2.txt", np.array([lv_esv]),fmt="%g")

    if save_ef:
        print("Saving EF!")
        # np.savetxt(f"{seg_pl.parent.parent}/multilabel_seg_analysis/LA_EF.txt", np.array([la_ef]))
        # np.savetxt(f"{seg_pl.parent.parent}/multilabel_seg_analysis/LV_EF.txt", np.array([lv_ef]))

        np.savetxt(f"{seg_pl.parent}/LA_EF_v2.txt", np.array([la_ef]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LV_EF_v2.txt", np.array([lv_ef]),fmt="%g")

    return la_ef, lv_ef

def calc_EF_v2_S206(multilabel_seg, save_volume=False, save_ef=False, save_image=False, nFrames=7):
    """
    v2 Function to calculate the ejection fraction from list of volumes (will likely be 10).
    
    Usage:
        * vol_ar: array of volumes over time frames. Length should be either 10 or 20.
        
    Output:
        * LA EF, LV EF

    Updates to v2:
        * Repeat the volume measurements for 2 cycle, like phasic strain results
         to better see which is min and max LA volume

        * Take min(LA volume) to be LA EDV
        * Take max(LA volume) to LA ESV

        Calculate LAEF from LA EDV and LA EDV instead of assuming 0th frame is LA EDV
    """

    ## Extract directory
    seg_pl = Path(multilabel_seg)

    ## First calculate volumes for all time frames
    # nFrames=10
    la_vols = np.zeros((nFrames,))
    lv_vols = np.zeros((nFrames,))

    frames=np.arange(10)
    frames=list(frames)
    frames.remove(1)
    frames.remove(2)
    frames.remove(4)
    print("frames: ", frames)

    for i, frame in enumerate(frames):
        print(f"Reading dcm-{frame}_label_maps.nii.gz")
        la_vols[i], lv_vols[i]=calc_volume(f"{seg_pl.parent}/dcm-{frame}_label_maps.nii.gz")
        print("LA volume: ", la_vols[i])

    ## Repeat cardiac cycle
    la_vols_list = list(la_vols)
    lv_vols_list = list(lv_vols)

    la_vols_list_repeat = la_vols_list + la_vols_list
    lv_vols_list_repeat = lv_vols_list + lv_vols_list

    ## Make plot
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    time = np.arange(0,nFrames*2)
    time = time/nFrames
    ax1.plot(time, la_vols_list_repeat)
    ax2.plot(time, lv_vols_list_repeat)

    ax1.set_ylabel("LA volume [ml]")
    ax2.set_ylabel("LV volume [ml]")
    ax2.set_xlabel("time (normalised)")

    plt.suptitle(f"{seg_pl.parent.parent.stem}")

    if save_image:
        print("Saving image!")
        plt.savefig(f"{seg_pl.parent}/la_lv_vol_transients_v2.png", 
                dpi=200, bbox_inches="tight")

    # plt.show()
    ## End plot

    ## Get index of largest volume in case of LA
    ## Get index of smallest volume in case of LV
    la_max_idx = np.argmax(la_vols)
    la_min_idx = np.argmin(la_vols)

    lv_max_idx = np.argmax(lv_vols)
    lv_min_idx = np.argmin(lv_vols)

    ## Calculate ejection fraction
    la_sv = la_vols[la_max_idx] - la_vols[la_min_idx]
    lv_sv = lv_vols[lv_max_idx] - lv_vols[lv_min_idx]

    ## Corrected LA_emptying fraction: LA max vol - LA min vol/LA max 
    la_ef = la_sv/la_vols[la_max_idx] * 100
    lv_ef = lv_sv/lv_vols[lv_max_idx] * 100

    if save_volume:
        print("Saving volumes!")
        np.savetxt(f"{seg_pl.parent}/la_volumes_v2.txt", la_vols,fmt="%g")
        np.savetxt(f"{seg_pl.parent}/lv_volumes_v2.txt", lv_vols,fmt="%g")

        np.savetxt(f"{seg_pl.parent}/LA_EDV_v2.txt", la_vols,fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LA_ESV_v2.txt", la_vols,fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LV_EDV_v2.txt", lv_vols,fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LV_ESV_v2.txt", lv_vols,fmt="%g")

    if save_ef:
        print("Saving EF!")
        # np.savetxt(f"{seg_pl.parent.parent}/multilabel_seg_analysis/LA_EF.txt", np.array([la_ef]))
        # np.savetxt(f"{seg_pl.parent.parent}/multilabel_seg_analysis/LV_EF.txt", np.array([lv_ef]))

        np.savetxt(f"{seg_pl.parent}/LA_EF_v2.txt", np.array([la_ef]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LV_EF_v2.txt", np.array([lv_ef]),fmt="%g")

    return la_ef, lv_ef

def calc_EF_v2_S148(multilabel_seg, save_volume=False, save_ef=False, save_image=False, nFrames=18):
    """
    v2 Function to calculate the ejection fraction from list of volumes (will likely be 10).
    
    Usage:
        * vol_ar: array of volumes over time frames. Length should be either 10 or 20.
        
    Output:
        * LA EF, LV EF

    Updates to v2:
        * Repeat the volume measurements for 2 cycle, like phasic strain results
         to better see which is min and max LA volume

        * Take min(LA volume) to be LA EDV
        * Take max(LA volume) to LA ESV

        Calculate LAEF from LA EDV and LA EDV instead of assuming 0th frame is LA EDV
    """

    ## Extract directory
    seg_pl = Path(multilabel_seg)

    ## First calculate volumes for all time frames
    # nFrames=10
    la_vols = np.zeros((nFrames,))
    lv_vols = np.zeros((nFrames,))

    frames=np.arange(20)
    frames=list(frames)
    frames.remove(2)
    frames.remove(11)
    print("frames: ", frames)

    for i, frame in enumerate(frames):
        print(f"Reading dcm-{frame}_label_maps.nii.gz")
        la_vols[i], lv_vols[i]=calc_volume(f"{seg_pl.parent}/dcm-{frame}_label_maps.nii.gz")
        print("LA volume: ", la_vols[i])

    ## Repeat cardiac cycle
    la_vols_list = list(la_vols)
    lv_vols_list = list(lv_vols)

    la_vols_list_repeat = la_vols_list + la_vols_list
    lv_vols_list_repeat = lv_vols_list + lv_vols_list

    ## Make plot
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    time = np.arange(0,nFrames*2)
    time = time/nFrames
    ax1.plot(time, la_vols_list_repeat)
    ax2.plot(time, lv_vols_list_repeat)

    ax1.set_ylabel("LA volume [ml]")
    ax2.set_ylabel("LV volume [ml]")
    ax2.set_xlabel("time (normalised)")

    plt.suptitle(f"{seg_pl.parent.parent.stem}")

    if save_image:
        print("Saving image!")
        plt.savefig(f"{seg_pl.parent}/la_lv_vol_transients_v2.png", 
                dpi=200, bbox_inches="tight")

    # plt.show()
    ## End plot

    ## Get index of largest volume in case of LA
    ## Get index of smallest volume in case of LV
    la_max_idx = np.argmax(la_vols)
    la_min_idx = np.argmin(la_vols)

    lv_max_idx = np.argmax(lv_vols)
    lv_min_idx = np.argmin(lv_vols)

    ## Calculate ejection fraction
    la_sv = la_vols[la_max_idx] - la_vols[la_min_idx]
    lv_sv = lv_vols[lv_max_idx] - lv_vols[lv_min_idx]

    ## Corrected LA_emptying fraction: LA max vol - LA min vol/LA max 
    la_ef = la_sv/la_vols[la_max_idx] * 100
    lv_ef = lv_sv/lv_vols[lv_max_idx] * 100

    if save_volume:
        print("Saving volumes!")
        np.savetxt(f"{seg_pl.parent}/la_volumes_v2.txt", la_vols,fmt="%g")
        np.savetxt(f"{seg_pl.parent}/lv_volumes_v2.txt", lv_vols,fmt="%g")

        np.savetxt(f"{seg_pl.parent}/LA_EDV_v2.txt", la_vols,fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LA_ESV_v2.txt", la_vols,fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LV_EDV_v2.txt", lv_vols,fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LV_ESV_v2.txt", lv_vols,fmt="%g")

    if save_ef:
        print("Saving EF!")
        # np.savetxt(f"{seg_pl.parent.parent}/multilabel_seg_analysis/LA_EF.txt", np.array([la_ef]))
        # np.savetxt(f"{seg_pl.parent.parent}/multilabel_seg_analysis/LV_EF.txt", np.array([lv_ef]))

        np.savetxt(f"{seg_pl.parent}/LA_EF_v2.txt", np.array([la_ef]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LV_EF_v2.txt", np.array([lv_ef]),fmt="%g")

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
    la_vols = np.zeros((nFrames-1,))
    lv_vols = np.zeros((nFrames-1,))

    frame_list=range(nFrames)
    frame_list=list(frame_list)
    frame_list.remove(1)

    # for i in range(0, nFrames):
    for i in frame_list:
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

    plt.suptitle(f"{seg_pl.parent.parent.stem}")
    
    if save_image:
        print("Saving image!")
        plt.savefig(f"{seg_pl.parent.parent}/multilabel_seg_analysis/vol_transients.png", 
                dpi=200, bbox_inches="tight")

    plt.show()

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

def calc_max_volume(multilabel_seg, nFrames=10):
    """
    This script calculates the maximum LA volume
    """

    ## First calculate volumes
    ## Extract directory
    seg_pl = Path(multilabel_seg)

    ## First calculate volumes for all time frames
    # nFrames=20
    la_vols = np.zeros((nFrames,))
    lv_vols = np.zeros((nFrames,))

    for i in range(0, nFrames):
        # print(f"Reading dcm-{i}_label_maps.nii.gz")
        la_vols[i], lv_vols[i]=calc_volume(f"{seg_pl.parent}/dcm-{i}_label_maps.nii.gz")
        # print("LA volume: ", la_vols[i])

    la_max_vol = max(la_vols)
    return la_max_vol

def LAEF_weird_idx_cases(multilabel_seg, save_ef=False, nFrames=10):
    """
    This script calculates the LAEF for cases with non sequential indexing
    """

    ## First calculate volumes
    ## Extract directory
    seg_pl = Path(multilabel_seg)

    ## Extract LA_vol.txt and LA_vol_max.txt
    la_vol_t0=np.loadtxt(f"{seg_pl.parent}/LA_vol.txt")
    la_vol_tmax=np.loadtxt(f"{seg_pl.parent}/LA_vol_max.txt")

    ## Extract LV_EDV.txt and LV_ESV.txt
    lv_esv=np.loadtxt(f"{seg_pl.parent}/LV_ESV.txt")
    lv_edv=np.loadtxt(f"{seg_pl.parent}/LV_EDV.txt")

    ## Calculate ejection fraction
    la_sv = la_vol_tmax - la_vol_t0
    lv_sv = lv_edv - lv_esv

    ## Corrected LA_emptying fraction: LA max vol - LA min vol/LA max 
    la_ef = la_sv/la_vol_tmax * 100
    lv_ef = lv_sv/lv_edv * 100

    if save_ef:
        print("Saving EF!")
        # np.savetxt(f"{seg_pl.parent.parent}/multilabel_seg_analysis/LA_EF.txt", np.array([la_ef]))
        # np.savetxt(f"{seg_pl.parent.parent}/multilabel_seg_analysis/LV_EF.txt", np.array([lv_ef]))

        np.savetxt(f"{seg_pl.parent}/LA_EF.txt", np.array([la_ef]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LV_EF.txt", np.array([lv_ef]),fmt="%g")

    return la_ef, lv_ef

if __name__ == '__main__':
    
    # Path to multilabel segmentation
    path=sys.argv[1]
    
    ## Uncomment here for LAEF and LVEF calculation
    # la, lv = calc_volume(path)
    # print("LA volume:", la)
    # print("LV volume:", lv)

    # print(la)
    # print(lv)
    # print("LA: ", la)
    # print("LV: ", lv)

    # la_ef, lv_ef = calc_EF(path, save_volume=False, save_ef=False, nFrames=10)
    # print("LA EF:", la_ef)
    # print("LV EF:", lv_ef)

    # plot_volumes(path, save_image=False, nFrames=10)

    # la = calc_max_volume(path, nFrames=10)
    # print(la)

    # vol = calc_volume_Manual(path)
    # print(vol)

    # lv_myo_vol = calc_LV_myo_volume(path)
    # print(lv_myo_vol)

    # la_ef, lv_ef = LAEF_weird_idx_cases(path, save_ef=True)
    # print(la_ef)
    # print(lv_ef)

    la_ef, lv_ef = calc_EF_v2(path, save_ef=True, save_image=True, save_volume=True, nFrames=20)
    print(la_ef)
    print(lv_ef)

    # la_ef, lv_ef = calc_EF_v2_S148(path, save_ef=True, save_image=True, save_volume=True)
    # print(la_ef)
    # print(lv_ef)