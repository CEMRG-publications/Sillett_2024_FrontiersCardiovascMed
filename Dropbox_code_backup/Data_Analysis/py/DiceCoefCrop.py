import numpy as np
import SimpleITK as sitk
import sys
import argparse
import nibabel as nib

parser = argparse.ArgumentParser()

parser.add_argument('--GT-seg', required=True, help='path to ground truth segmentation (.nii)')
parser.add_argument('--tracked-seg', required=True, help='path to tracked segmentation (.nii)')

args = parser.parse_args()

# dcm4_Seg = str(sys.argv[1])
# trk_Seg = str(sys.argv[2])

def diceCoefCrop(Path2dcm4_Seg, Path2trk_Seg, smooth=1):
    
    y_true = sitk.ReadImage(Path2dcm4_Seg)
    y_pred = sitk.ReadImage(Path2trk_Seg)
    
    y_true = sitk.GetArrayFromImage(y_true)
    y_pred = sitk.GetArrayFromImage(y_pred)
    
    y_true[y_true==3] = 0
    y_pred[y_pred==3] = 0
    
    y_true_f = y_true.flatten()
    y_pred_f = y_pred.flatten()
    intersection = np.sum(y_true_f * y_pred_f)
    dice_coef = (2. * intersection + smooth) / (np.sum(y_true_f) + np.sum(y_pred_f) + smooth)
    return dice_coef

def diceCoef_crt31_34(Path2dcm4_Seg, Path2trk_Seg, smooth=1):

    ## Used this function to calculate DSC for crt31 and 34
    
    y_true = nib.load(Path2dcm4_Seg)
    y_pred = nib.load(Path2trk_Seg)
    
    y_true = np.array(y_true.dataobj)
    y_pred = np.array(y_pred.dataobj)

    ## Need to do this to normalise DSC
    y_true = np.rint(y_true)
    y_pred = np.rint(y_pred)
    y_true[y_true!=4] = 0.0
    y_pred[y_pred!=4] = 0.0
    y_true[y_true==4] = 1.0
    y_pred[y_pred==4] = 1.0

    # print(np.max(y_true))
    # print(np.max(y_pred))    

    # print("y_true shape", y_true.shape)
    # print("y_pred shape", y_pred.shape)
    
    y_true_f = y_true.flatten()
    y_pred_f = y_pred.flatten()

    # print(max(y_true_f))
    # print(max(y_pred_f))

    intersection = np.sum(y_true_f * y_pred_f)
    dice_coef = (2. * intersection + smooth) / (np.sum(y_true_f) + np.sum(y_pred_f) + smooth)

    # print("intersection: ", intersection)

    # print("Numerator: ", (2. * intersection + smooth))
    # print("Denominator: ", (np.sum(y_true_f) + np.sum(y_pred_f) + smooth))
    return dice_coef

dice = diceCoef_crt31_34(args.GT_seg, args.tracked_seg)
dice = diceCoefCrop(args.GT_seg, args.tracked_seg)

print(dice)