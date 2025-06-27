import numpy as np
import SimpleITK as sitk
import sys
import nibabel as nib

def diceCoef(Path2dcm4_Seg, Path2trk_Seg, smooth=1):
    
    y_true = sitk.ReadImage(Path2dcm4_Seg)
    y_pred = sitk.ReadImage(Path2trk_Seg)
    
    y_true = sitk.GetArrayFromImage(y_true)
    y_pred = sitk.GetArrayFromImage(y_pred)
    
    y_true_f = y_true.flatten()
    y_pred_f = y_pred.flatten()
    intersection = np.sum(y_true_f * y_pred_f)
    dice_coef = (2. * intersection + smooth) / (np.sum(y_true_f) + np.sum(y_pred_f) + smooth)
    return dice_coef

def diceCoef_crt31_34(Path2dcm4_Seg, Path2trk_Seg, smooth=1):

	## Used this function to calculate DSC for crt31 and 34
	##
    
    y_true = nib.load(Path2dcm4_Seg)
    y_pred = nib.load(Path2trk_Seg)
    
    y_true = np.array(y_true.dataobj)
    y_pred = np.array(y_pred.dataobj)

    y_true[y_true==4.0] = 1
    y_pred[y_pred==4.0] = 1

    # print("y_true shape", y_true.shape)
    # print("y_pred shape", y_pred.shape)
    
    y_true_f = y_true.flatten()
    y_pred_f = y_pred.flatten()

    # print(max(y_true_f))
    # print(max(y_pred_f))

    intersection = np.sum(y_true_f * y_pred_f)
    dice_coef = (2. * intersection + smooth) / (np.sum(y_true_f) + np.sum(y_pred_f) + smooth)
    return dice_coef

def diceCoef_RV(Path2dcm4_Seg, Path2trk_Seg, smooth=1):

    ## Used this function to calculate DSC for crt31 and 34
    ##
    
    y_true = nib.load(Path2dcm4_Seg)
    y_pred = nib.load(Path2trk_Seg)
    
    y_true = np.array(y_true.dataobj)
    y_pred = np.array(y_pred.dataobj)

    y_true[y_true==3.0] = 1
    y_pred[y_pred==3.0] = 1

    # print("y_true shape", y_true.shape)
    # print("y_pred shape", y_pred.shape)
    
    y_true_f = y_true.flatten()
    y_pred_f = y_pred.flatten()

    # print(max(y_true_f))
    # print(max(y_pred_f))

    intersection = np.sum(y_true_f * y_pred_f)
    dice_coef = (2. * intersection + smooth) / (np.sum(y_true_f) + np.sum(y_pred_f) + smooth)
    return dice_coef

if __name__ == "__main__":
    
    dcm4_Seg = str(sys.argv[1])
    trk_Seg = str(sys.argv[2])

    # dice = diceCoef_crt31_34(dcm4_Seg, trk_Seg)
    dice = diceCoef_RV(dcm4_Seg, trk_Seg)
    
    print(dice)