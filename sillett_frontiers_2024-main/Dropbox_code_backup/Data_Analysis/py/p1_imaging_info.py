## Script to finding imaging properties for P1

import SimpleITK as sitk

import sys

## path to nifti img
path=sys.argv[1]


img = sitk.ReadImage(path)
img_ar = sitk.GetArrayFromImage(img)
dim = img_ar.shape
res = img.GetSpacing()

print("IMG: ", path)
print("Shape: ", dim)
print("Resolution: ", res)