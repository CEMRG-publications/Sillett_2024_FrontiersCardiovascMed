
# IN PROGRESS: Define function to exrtact LA label from Hao's label maps

import numpy as np
import SimpleITK as sitk
import sys

label_map = str(sys.argv[1])

def LA_label_extract(Path2Label_map):
    
    labels = sitk.ReadImage(Path2Label_map)
    
    labels = sitk.GetArrayFromImage(y_true)
    
    labels[labels!=4] = 0

    LA_label = sitk.GetImageFromArray(labels)
    
    return LA_label

dice = diceCoefCrop(dcm4_Seg, trk_Seg)

print(dice)