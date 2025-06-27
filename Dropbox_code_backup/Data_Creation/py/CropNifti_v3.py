## Tring to dbug stanford cases with cropping error.

import nibabel as nib
import numpy as np
import sys
import os
if len(sys.argv) != 9:
  print("Usage: " + sys.argv[0] + " inputImage outputImage index.x index.y index.z size.x size.y size.z")
  sys.exit(1)
print("extract_image_filter %s" % sys.argv[1])
print("output: %s" % sys.argv[2])

input_filename = sys.argv[1]
basename = os.path.basename(input_filename)
filename = os.path.splitext(basename)[0]
output_filename = sys.argv[2]
index_x = int(sys.argv[3])
index_y = int(sys.argv[4])
index_z = int(sys.argv[5])
size_x = int(sys.argv[6])
size_y = int(sys.argv[7])
size_z = int(sys.argv[8])

## Load image
img = nib.load(input_filename)
print("original image shape: ", img.shape)

img_ar = img.dataobj
img_ar = img_ar[index_x:index_x+size_x, index_y:index_y+size_y, index_z:index_z+size_z]
print("cropped image shape: ", img_ar.shape)

affine_crop = np.copy(img.affine)
affine_crop[0, 3] = img.affine[0, 3]-index_x*np.abs(img.affine[0,0])
affine_crop[1, 3] = img.affine[1, 3]+index_y*np.abs(img.affine[1,1])
affine_crop[2, 3] = img.affine[2, 3]+index_z*np.abs(img.affine[2,2])

print("original affine matrix:\n", img.affine)
print("crop affine matrix:\n", affine_crop)

final_img = nib.Nifti1Image(img_ar, affine=affine_crop)
nib.save(final_img, output_filename)