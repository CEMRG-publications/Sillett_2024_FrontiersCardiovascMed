import sys
import numpy as np
import SimpleITK as sitk

Path2Image = str(sys.argv[1])

image = sitk.ReadImage(Path2Image)
pixel_dim_tuple = image.GetSpacing()

print(round(pixel_dim_tuple[0],2), round(pixel_dim_tuple[1],2), round(pixel_dim_tuple[2],2))