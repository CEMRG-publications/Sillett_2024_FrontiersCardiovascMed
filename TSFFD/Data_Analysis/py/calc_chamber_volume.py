### Script to calculate ejection fraction of LA, LV
###
###

import argparse
import sys
import nibabel as nib
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import pyvista as pv
import pandas as pd

### Functions to calculate:
 # volume of a segmentation using image resolution
 # ejection fraction


def calc_volume(multilabel_seg):
    """
    Function to return LA, LV, RV and RA volumes from HaoNet multilabel segmentation
    
    Usage:
        * Input: path to multilabel segmentation from HaoNet
        * Output: LA_volume, LV_volume, RV_volume, RA_volume [ml]
    """
    
    ## Read in multilabel_seg as array
    seg = nib.load(multilabel_seg)
    seg_ar = seg.get_fdata()

    ## Calculate voxel volume in multilabel_seg (same as the original nifti image)
    mat = seg.affine
    vxl_vol = np.abs(mat[0,0]*mat[1,1]*mat[2,2])
    
    ## Labels for LV BP, LA and RV
    labels=[1.0, 4.0, 3.0, 5.0]  ## [LV_label, LA_label, RV_label, RA_label]
    vol=np.zeros((len(labels),))
    for i in range(0,len(labels)):
        target_label=labels[i]

        ## Count number of voxels with target_label in multilabel_seg_ar
        n_vxls = np.count_nonzero(seg_ar==target_label)

        ## Calc volume for given label
        vol[i] = n_vxls*vxl_vol

    ## Convert to ml
    vol = vol * 1e-3

    ## Check multilabel labels for LA and LV
    LV_vol = vol[0]
    LA_vol = vol[1]
    RV_vol = vol[2]
    RA_vol = vol[3]

    return LA_vol, LV_vol, RV_vol, RA_vol

def calc_volume_LAA(multilabel_seg):
    """
    Function to return LAA volume from HaoNet multilabel segmentation
    
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
    
    ## Labels for LV BP, LA and RV
    labels=[10.0]  ## [LV_label, LA_label, RV_label]
    vol=np.zeros((len(labels),))
    for i in range(0,len(labels)):
        target_label=labels[i]

        ## Count number of voxels with target_label in multilabel_seg_ar
        n_vxls = np.count_nonzero(seg_ar==target_label)

        ## Calc volume for given label
        vol[i] = n_vxls*vxl_vol

    ## Convert to ml
    vol = vol * 1e-3

    ## Check multilabel labels for LA and LV
    LAA_vol = vol[0]

    return LAA_vol

def calc_area_LAA(path2msh):
    """
    Function to return LAA surface areas from tracked cLr meshes
    
    Usage:
        * Input: path to a cLr mesh (e.g. cLr-aligned-0.vtp)
        * Output: LAA surface area of input msh
    """
    
    ## Read in initial cLr-aligned-0 mesh
    msh = pv.read(path2msh)
    elemTag=msh.cell_data['elemTag']

    # Calculate cell sizes (areas)
    sized=msh.compute_cell_sizes()
    cell_areas=sized.cell_data['Area']

    # Get cell areas for LAA label
    cell_areas_laa=cell_areas[elemTag == 19.0]

    # Sum cell areas
    LAA_surface_area = cell_areas_laa.sum()

    return LAA_surface_area

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

def calc_EF_v2(multilabel_seg, save_volume=False, save_ef=False, save_image=False, nFrames=20, append_result=False):
    """
    v2 Function to calculate the ejection fraction from list of volumes (will likely be 10).
    Vitaliy Analysis update: include RV and RA
    
    Usage:
        * vol_ar: array of volumes over time frames. Length should be either 10 or 20.
        
    Output:
        * LA EF, LV EF, RV EF, RA_EF

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
    rv_vols = np.zeros((nFrames,))
    ra_vols = np.zeros((nFrames,))

    # frame_list=range(nFrames)
    # frame_list=list(frame_list)
    # frame_list.remove(1)

    # frame_num = np.arange(20, 120, 10)

    for i in range(0, nFrames):
        print(f"Reading dcm-{i}_label_maps.nii.gz")
        la_vols[i], lv_vols[i], rv_vols[i], ra_vols[i] =calc_volume(f"{seg_pl.parent}/dcm-{i}_label_maps.nii.gz")
        print("LA volume: ", la_vols[i])
        print("LV volume: ", lv_vols[i])
        print("RV volume: ", rv_vols[i])
        print("RA volume: ", ra_vols[i])

    ## Repeat cardiac cycle
    la_vols_list = list(la_vols)
    lv_vols_list = list(lv_vols)
    rv_vols_list = list(rv_vols)
    ra_vols_list = list(ra_vols)

    la_vols_list_repeat = la_vols_list + la_vols_list
    lv_vols_list_repeat = lv_vols_list + lv_vols_list
    rv_vols_list_repeat = rv_vols_list + rv_vols_list
    ra_vols_list_repeat = ra_vols_list + ra_vols_list

    ## Make plot
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True)

    time = np.arange(0,nFrames*2)
    time = time/nFrames
    ax1.plot(time, la_vols_list_repeat)
    ax2.plot(time, lv_vols_list_repeat)
    ax3.plot(time, rv_vols_list_repeat)
    ax4.plot(time, ra_vols_list_repeat)

    ax1.grid(True)
    ax2.grid(True)
    ax3.grid(True)
    ax4.grid(True)

    ax1.set_ylabel("LA\nvolume [ml]")
    ax2.set_ylabel("LV\nvolume [ml]")
    ax3.set_ylabel("RV\nvolume [ml]")
    ax4.set_ylabel("RA\nvolume [ml]")
    ax4.set_xlabel("frame")

    # print(time)
    tick_labels=list(range(20))
    tick_labels=tick_labels+tick_labels
    ax4.set_xticks(ticks=np.arange(0, 2, 0.05))
    ax4.set_xticklabels(tick_labels)

    ax4.set_xlim(-0.05, 1.0)

    plt.suptitle(f"{seg_pl.parent.parent.stem}")
    plt.tight_layout()

    if save_image:
        print("Saving image!")
        plt.savefig(f"{seg_pl.parent}/la_lv_rv_ra_vol_transients_v2.png", 
                dpi=200, bbox_inches="tight")

    # plt.show()
    ## End plot

    ## Get index of largest volume in case of LA
    ## Get index of smallest volume in case of LV
    la_max_idx = np.argmax(la_vols)
    la_min_idx = np.argmin(la_vols)

    lv_max_idx = np.argmax(lv_vols)
    lv_min_idx = np.argmin(lv_vols)

    rv_max_idx = np.argmax(rv_vols)
    rv_min_idx = np.argmin(rv_vols)

    ra_max_idx = np.argmax(ra_vols)
    ra_min_idx = np.argmin(ra_vols)

    ## Calculate ejection fraction
    la_sv = la_vols[la_max_idx] - la_vols[la_min_idx]
    lv_sv = lv_vols[lv_max_idx] - lv_vols[lv_min_idx]
    rv_sv = rv_vols[rv_max_idx] - rv_vols[rv_min_idx]
    ra_sv = ra_vols[ra_max_idx] - ra_vols[ra_min_idx]

    ## Corrected LA_emptying fraction: LA max vol - LA min vol/LA max 
    la_ef = la_sv/la_vols[la_max_idx] * 100
    lv_ef = lv_sv/lv_vols[lv_max_idx] * 100
    rv_ef = rv_sv/rv_vols[rv_max_idx] * 100
    ra_ef = ra_sv/ra_vols[ra_max_idx] * 100

    la_edv = la_vols[la_min_idx]
    la_esv = la_vols[la_max_idx]

    lv_edv = lv_vols[lv_max_idx]
    lv_esv = lv_vols[lv_min_idx]

    rv_edv = rv_vols[rv_max_idx]
    rv_esv = rv_vols[rv_min_idx]

    ra_edv = ra_vols[ra_min_idx]
    ra_esv = ra_vols[ra_max_idx]

    if save_volume:
        print("Saving volumes!")
        np.savetxt(f"{seg_pl.parent}/la_volumes_v2.txt", la_vols,fmt="%g")
        np.savetxt(f"{seg_pl.parent}/lv_volumes_v2.txt", lv_vols,fmt="%g")
        np.savetxt(f"{seg_pl.parent}/rv_volumes_v2.txt", rv_vols,fmt="%g")
        np.savetxt(f"{seg_pl.parent}/ra_volumes_v2.txt", ra_vols,fmt="%g")

        np.savetxt(f"{seg_pl.parent}/LA_EDV_v2.txt", np.array([la_edv]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LA_ESV_v2.txt", np.array([la_esv]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LV_EDV_v2.txt", np.array([lv_edv]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LV_ESV_v2.txt", np.array([lv_esv]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/RV_EDV_v2.txt", np.array([rv_edv]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/RV_ESV_v2.txt", np.array([rv_esv]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/RA_EDV_v2.txt", np.array([ra_edv]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/RA_ESV_v2.txt", np.array([ra_esv]),fmt="%g")

    if save_ef:
        print("Saving EF!")
        # np.savetxt(f"{seg_pl.parent.parent}/multilabel_seg_analysis/LA_EF.txt", np.array([la_ef]))
        # np.savetxt(f"{seg_pl.parent.parent}/multilabel_seg_analysis/LV_EF.txt", np.array([lv_ef]))

        np.savetxt(f"{seg_pl.parent}/LA_EF_v2.txt", np.array([la_ef]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LV_EF_v2.txt", np.array([lv_ef]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/RV_EF_v2.txt", np.array([rv_ef]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/RA_EF_v2.txt", np.array([ra_ef]),fmt="%g")

    if append_result:
        print("Appending results to master df!")
        path2csv="/home/csi20/Dropbox/phd/Projects/Vitaliy/VA_Results(2)-loaded_v2.xlsx"
        df=pd.read_excel(path2csv, index_col=0)

        case=seg_pl.parent.parent.stem
        print("case", case)

        chamber_list=["RV", "LV", "RA", "LA"]
        metrics_list=["EDV", "ESV", "EF"]

        results= [
            [rv_edv, rv_esv, rv_ef],
            [lv_edv, lv_esv, lv_ef],
            [ra_edv, ra_esv, ra_ef],
            [la_edv, la_esv, la_ef]
        ]

        for i, chamber in enumerate(chamber_list):
            for j, metric in enumerate(metrics_list):    
                df.loc[case, f"{chamber} {metric}"]=results[i][j]

        ## Save
        path2csv_pl=Path(path2csv)
        df.to_excel(path2csv)

    return la_ef, lv_ef, rv_ef, ra_ef

def calc_EF_v2_skipframe(multilabel_seg, frame_to_skip, save_volume=False, save_ef=False, save_image=False, nFrames=20, append_result=False):
    """
    v2 Function to calculate the ejection fraction from list of volumes (will likely be 10).
    Vitaliy Analysis update: include RV and RA
    
    Usage:
        * vol_ar: array of volumes over time frames. Length should be either 10 or 20.
        
    Output:
        * LA EF, LV EF, RV EF, RA_EF

    Updates to v2:
        * Repeat the volume measurements for 2 cycle, like phasic strain results
         to better see which is min and max LA volume

        * Take min(LA volume) to be LA EDV
        * Take max(LA volume) to LA ESV

        Calculate LAEF from LA EDV and LA EDV instead of assuming 0th frame is LA EDV
    """

    ## Extract directory
    seg_pl = Path(multilabel_seg)

    frame_list=range(nFrames)
    frame_list=list(frame_list)
    frame_list.remove(frame_to_skip)

    ## First calculate volumes for all time frames
    # nFrames=10
    la_vols = np.zeros((len(frame_list),))
    lv_vols = np.zeros((len(frame_list),))
    rv_vols = np.zeros((len(frame_list),))
    ra_vols = np.zeros((len(frame_list),))

    # frame_num = np.arange(20, 120, 10)

    for i, frame in enumerate(frame_list):
        print(f"Reading dcm-{frame}_label_maps.nii.gz")
        la_vols[i], lv_vols[i], rv_vols[i], ra_vols[i] =calc_volume(f"{seg_pl.parent}/dcm-{frame}_label_maps.nii.gz")
        print("LA volume: ", la_vols[i])
        print("LV volume: ", lv_vols[i])
        print("RV volume: ", rv_vols[i])
        print("RA volume: ", ra_vols[i])

    ## Repeat cardiac cycle
    la_vols_list = list(la_vols)
    lv_vols_list = list(lv_vols)
    rv_vols_list = list(rv_vols)
    ra_vols_list = list(ra_vols)

    la_vols_list_repeat = la_vols_list + la_vols_list
    lv_vols_list_repeat = lv_vols_list + lv_vols_list
    rv_vols_list_repeat = rv_vols_list + rv_vols_list
    ra_vols_list_repeat = ra_vols_list + ra_vols_list

    ## Make plot
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True)

    time = np.arange(0,len(frame_list)*2)
    time = time/nFrames
    ax1.plot(time, la_vols_list_repeat)
    ax2.plot(time, lv_vols_list_repeat)
    ax3.plot(time, rv_vols_list_repeat)
    ax4.plot(time, ra_vols_list_repeat)

    ax1.grid(True)
    ax2.grid(True)
    ax3.grid(True)
    ax4.grid(True)

    ax1.set_ylabel("LA\nvolume [ml]")
    ax2.set_ylabel("LV\nvolume [ml]")
    ax3.set_ylabel("RV\nvolume [ml]")
    ax4.set_ylabel("RA\nvolume [ml]")
    ax4.set_xlabel("frame")

    # print(time)
    tick_labels=frame_list
    tick_labels=tick_labels+tick_labels
    # ax4.set_xticks(ticks=np.arange(0, 2, 0.05))
    # ax4.set_xticklabels(tick_labels)

    ax4.set_xlim(-0.05, 1.0)

    plt.suptitle(f"{seg_pl.parent.parent.stem}")
    plt.tight_layout()

    if save_image:
        print("Saving image!")
        plt.savefig(f"{seg_pl.parent}/la_lv_rv_ra_vol_transients_v2.png", 
                dpi=200, bbox_inches="tight")

    # plt.show()
    ## End plot

    ## Get index of largest volume in case of LA
    ## Get index of smallest volume in case of LV
    la_max_idx = np.argmax(la_vols)
    la_min_idx = np.argmin(la_vols)

    lv_max_idx = np.argmax(lv_vols)
    lv_min_idx = np.argmin(lv_vols)

    rv_max_idx = np.argmax(rv_vols)
    rv_min_idx = np.argmin(rv_vols)

    ra_max_idx = np.argmax(ra_vols)
    ra_min_idx = np.argmin(ra_vols)

    ## Calculate ejection fraction
    la_sv = la_vols[la_max_idx] - la_vols[la_min_idx]
    lv_sv = lv_vols[lv_max_idx] - lv_vols[lv_min_idx]
    rv_sv = rv_vols[rv_max_idx] - rv_vols[rv_min_idx]
    ra_sv = ra_vols[ra_max_idx] - ra_vols[ra_min_idx]

    ## Corrected LA_emptying fraction: LA max vol - LA min vol/LA max 
    la_ef = la_sv/la_vols[la_max_idx] * 100
    lv_ef = lv_sv/lv_vols[lv_max_idx] * 100
    rv_ef = rv_sv/rv_vols[rv_max_idx] * 100
    ra_ef = ra_sv/ra_vols[ra_max_idx] * 100

    la_edv = la_vols[la_min_idx]
    la_esv = la_vols[la_max_idx]

    lv_edv = lv_vols[lv_max_idx]
    lv_esv = lv_vols[lv_min_idx]

    rv_edv = rv_vols[rv_max_idx]
    rv_esv = rv_vols[rv_min_idx]

    ra_edv = ra_vols[ra_min_idx]
    ra_esv = ra_vols[ra_max_idx]

    if save_volume:
        print("Saving volumes!")
        np.savetxt(f"{seg_pl.parent}/la_volumes_v2.txt", la_vols,fmt="%g")
        np.savetxt(f"{seg_pl.parent}/lv_volumes_v2.txt", lv_vols,fmt="%g")
        np.savetxt(f"{seg_pl.parent}/rv_volumes_v2.txt", rv_vols,fmt="%g")
        np.savetxt(f"{seg_pl.parent}/ra_volumes_v2.txt", ra_vols,fmt="%g")

        np.savetxt(f"{seg_pl.parent}/LA_EDV_v2.txt", np.array([la_edv]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LA_ESV_v2.txt", np.array([la_esv]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LV_EDV_v2.txt", np.array([lv_edv]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LV_ESV_v2.txt", np.array([lv_esv]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/RV_EDV_v2.txt", np.array([rv_edv]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/RV_ESV_v2.txt", np.array([rv_esv]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/RA_EDV_v2.txt", np.array([ra_edv]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/RA_ESV_v2.txt", np.array([ra_esv]),fmt="%g")

    if save_ef:
        print("Saving EF!")
        # np.savetxt(f"{seg_pl.parent.parent}/multilabel_seg_analysis/LA_EF.txt", np.array([la_ef]))
        # np.savetxt(f"{seg_pl.parent.parent}/multilabel_seg_analysis/LV_EF.txt", np.array([lv_ef]))

        np.savetxt(f"{seg_pl.parent}/LA_EF_v2.txt", np.array([la_ef]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/LV_EF_v2.txt", np.array([lv_ef]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/RV_EF_v2.txt", np.array([rv_ef]),fmt="%g")
        np.savetxt(f"{seg_pl.parent}/RA_EF_v2.txt", np.array([ra_ef]),fmt="%g")

    if append_result:
        print("Appending results to master df!")
        path2csv="/home/csi20/Dropbox/phd/Projects/Vitaliy/VA_Results(2)-loaded_v2.xlsx"
        df=pd.read_excel(path2csv, index_col=0)

        case=seg_pl.parent.parent.stem
        print("case", case)

        chamber_list=["RV", "LV", "RA", "LA"]
        metrics_list=["EDV", "ESV", "EF"]

        results= [
            [rv_edv, rv_esv, rv_ef],
            [lv_edv, lv_esv, lv_ef],
            [ra_edv, ra_esv, ra_ef],
            [la_edv, la_esv, la_ef]
        ]

        for i, chamber in enumerate(chamber_list):
            for j, metric in enumerate(metrics_list):    
                df.loc[case, f"{chamber} {metric}"]=results[i][j]

        ## Save
        path2csv_pl=Path(path2csv)
        df.to_excel(path2csv)

    return la_ef, lv_ef, rv_ef, ra_ef

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

def plot_volumes_allchambers(multilabel_seg, save_image=False, nFrames=20):
    """
    This script plots volume transients for the: LA, LV, RV, and RA.
    Used for Vitaliy project analysis.
    """

    ## First calculate volumes
    ## Extract directory
    seg_pl = Path(multilabel_seg)

    ## First calculate volumes for all time frames
    # nFrames=20
    la_vols = np.zeros((nFrames,))
    lv_vols = np.zeros((nFrames,))
    rv_vols = np.zeros((nFrames,))
    ra_vols = np.zeros((nFrames,))

    frame_list=range(nFrames)

    # for i in range(0, nFrames):
    for i in frame_list:
        print(f"Reading dcm-{i}_label_maps.nii.gz")
        la_vols[i], lv_vols[i], rv_vols[i], ra_vols[i]=calc_volume(f"{seg_pl.parent}/dcm-{i}_label_maps.nii.gz")

    ## Make plot
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True)

    time = np.arange(0,nFrames)
    time = time/nFrames
    ax1.plot(time, la_vols)
    ax2.plot(time, lv_vols)
    ax3.plot(time, rv_vols)
    ax4.plot(time, ra_vols)

    ax1.set_ylabel("LA\nvolume [ml]")
    ax2.set_ylabel("LV\nvolume [ml]")
    ax3.set_ylabel("RV\nvolume [ml]")
    ax4.set_ylabel("RA\nvolume [ml]")
    ax4.set_xlabel("frame")

    # Set custom xtick positions
    xtick_positions = np.arange(start=0, stop=1, step=0.05)
    ax4.set_xticks(xtick_positions)

    # Set custom xtick labels
    xtick_labels = list(range(20))
    ax4.set_xticklabels(xtick_labels)

    for ax in fig.axes:
        ax.grid(True)

    plt.suptitle(f"{seg_pl.parent.parent.stem}")

    plt.tight_layout()
    
    if save_image:
        print("Saving image!")
        plt.savefig(f"{seg_pl.parent.parent}/la_lv_rv_ra_vol_transients.png", 
                dpi=200, bbox_inches="tight")

    plt.show()

def plot_volumes_LAA(multilabel_seg, save_image=False, nFrames=10):
    """
    This script plots 2 subplots for LAA analysis.
    
    Firstly, volume transients for LAA.
    Secondly, surface area transients from tracked cLr meshes
    """

    ## First calculate volumes
    ## Extract directory
    seg_pl = Path(multilabel_seg)

    ## First calculate volumes for all time frames
    # nFrames=20
    laa_vols = np.zeros((nFrames,))
    
    frame_list=range(nFrames)
    frame_list=list(frame_list)
    # frame_list.remove(1)

    # for i in range(0, nFrames):
    for i in frame_list:
        print(f"Reading dcm-{i}_label_maps.nii.gz")
        laa_vols[i]=calc_volume_LAA(f"{seg_pl.parent}/dcm-{i}_label_maps.nii.gz")
        # print("LA volume: ", la_vols[i])
        
    ## Make plot
    fig, ax1 = plt.subplots(1, 1, sharex=True)

    time = np.arange(0,nFrames)
    time = time/nFrames
    ax1.plot(time, laa_vols)

    ax1.set_ylabel("LAA volume [ml]")
    ax1.set_xlabel("time (normalised)")

    plt.suptitle(f"{seg_pl.parent.parent.stem}")
    
    if save_image:
        print("Saving image!")
        plt.savefig(f"{seg_pl.parent.parent}/nifti/laa_vol_transients.png", 
                dpi=200, bbox_inches="tight")

    plt.show()

def plot_areas_LAA(clr_msh, save_image=False, nFrames=10):
    """
    This script plots areas for LAA analysis.
    
    Firstly, volume transients for LAA.
    Secondly, surface area transients from tracked cLr meshes
    """

    ## First calculate volumes
    ## Extract directory
    msh_pl = Path(clr_msh)

    ## First calculate volumes for all time frames
    # nFrames=20
    laa_areas = np.zeros((10,))
    
    frame_list=range(10)
    frame_list=list(frame_list)
    # frame_list.remove(1)

    # for i in range(0, nFrames):
    for i in frame_list:
        # print("LA volume: ", la_vols[i])
        print(f"Reading cLr-aligned-{i}.vtp")
        laa_areas[i]=calc_area_LAA(f"{msh_pl.parent}/cLr-aligned-{i}.vtp")

    ## Make plot
    fig, ax1 = plt.subplots(1, 1, sharex=True)

    time = np.arange(0,nFrames)
    time = time/nFrames
    ax1.plot(time, laa_areas)

    ax1.set_ylabel("LAA area")
    ax1.set_xlabel("time (normalised)")

    plt.suptitle(f"{msh_pl.parent.parent.stem}")
    
    if save_image:
        print("Saving image!")
        plt.savefig(f"{msh_pl.parent}/laa_area_transients.png", 
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

def calc_LV_Myo_volume(multilabel_seg, save_volume=False,  append_result=False):
    """
    Function to return LV_Myo volumes from HaoNet multilabel segmentation
    
    Usage:
        * Input: path to multilabel segmentation from HaoNet
        * Output: LV_Myo volume [ml]
    """
    
    ## Read in multilabel_seg as array
    seg = nib.load(multilabel_seg)
    seg_ar = seg.get_fdata()

    ## Calculate voxel volume in multilabel_seg (same as the original nifti image)
    mat = seg.affine
    vxl_vol = np.abs(mat[0,0]*mat[1,1]*mat[2,2])
    
    ## Labels
    labels=[2.0]  ## LV_Myo_label
    vol=np.zeros((len(labels),))
    for i in range(0,len(labels)):
        target_label=labels[i]

        ## Count number of voxels with target_label in multilabel_seg_ar
        n_vxls = np.count_nonzero(seg_ar==target_label)

        ## Calc volume for given label
        vol[i] = n_vxls*vxl_vol

    ## Convert to ml
    vol = vol * 1e-3

    ## Check multilabel labels for LA and LV
    LV_Myo_vol = vol[0]

    seg_pl=Path(path)

    if save_volume:
        print("Saving LV Myo volume!")
        
        np.savetxt(f"{seg_pl.parent}/LV_Myo_volume.txt", np.array([LV_Myo_vol]),fmt="%g")

    if append_result:
        print("Appending results to master df!")
        path2csv="/home/csi20/Dropbox/phd/Projects/Vitaliy/AS_Staging_Results/AS_Staging_Data.xlsx"
        df=pd.read_excel(path2csv, index_col=0)

        case=seg_pl.parent.parent.stem
        print("case", case)

        df.loc[case, f"LV_Myo_Mass"]=LV_Myo_vol

        ## Save
        df.to_excel(path2csv)

    return LV_Myo_vol

if __name__ == '__main__':
    
    # Path to multilabel segmentation
    path=sys.argv[1]
    # numFrames=sys.argv[2]

    # la_ef, lv_ef, rv_ef, ra_ef = calc_EF_v2(path, save_ef=True, save_image=True, save_volume=True, nFrames=20, append_result=True)    
    # la_ef, lv_ef, rv_ef, ra_ef = calc_EF_v2_skipframe(path, frame_to_skip=4, save_ef=True, save_image=True, save_volume=True, nFrames=20, append_result=False)
    # print(la_ef)
    # print(lv_ef)
    # print(rv_ef)
    # print(ra_ef)

    # plot_volumes_LAA(path, True, nFrames=int(numFrames))
    # plot_areas_LAA(path, True)

    # la_ef, lv_ef = calc_EF_v2_S148(path, save_ef=True, save_image=True, save_volume=True)
    # print(la_ef)
    # print(lv_ef)

    ## Calculate volumes for LV_Myo for VA analysis Sept 2024
    lv_myo_vol = calc_LV_Myo_volume(path, save_volume=True, append_result=True)
    print(lv_myo_vol)