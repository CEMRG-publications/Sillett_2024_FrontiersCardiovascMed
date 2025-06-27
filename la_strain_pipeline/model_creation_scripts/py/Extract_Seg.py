  ## RR VT Case 17/01

import SimpleITK as sitk
import numpy as np
import nibabel as nib
import os, sys

def Get_LV_BP_label(Path2Img):
    
	"""
	Retrieves LV bloodpool label. 
	Use for constructing endocardial surface mesh
	"""

	img = nib.load(Path2Img)
	img_array = img.get_fdata()
	img_array[img_array!=1] = 0.0 #Sets all other labels other than LV BP label to zero
	img_nifti = nib.Nifti1Image(img_array, img.affine)

	return img_nifti

def Get_LV_MYO_label(Path2Img):

	"""
	Retrieves LV Myocardium label. 
	"""

	img = nib.load(Path2Img)
	img_array = img.get_fdata()

	img_array[img_array!=2] = 0.0 #Sets all other labels other than LV MYO label to zero
	
	img_nifti = nib.Nifti1Image(img_array, img.affine)

	return img_nifti

def Get_LV_BP_MYO_label(Path2Img):

	"""
	Retrieves LV bloodpool and myocardium labels joined together.
	Use for constructing epicardial surface mesh 
	"""

	img = nib.load(Path2Img)
	img_array = img.get_fdata()
	img_array[img_array==2] = 1 #Sets LV MYO to LV BP labels
	img_array[img_array!=1] = 0.0
	img_nifti = nib.Nifti1Image(img_array, img.affine)

	return img_nifti

def Get_LA_label(Path2Img):

	"""
	Retrieves LA bloodpool, PVs and LAA labels joined together.
	Use for constructing LA mesh with PVs and LAA included 
	"""

	img = nib.load(Path2Img)
	img_array = img.get_fdata()
	img_array[img_array==8] = 4   #Joins LAA, PVs to LA label
	img_array[img_array==9] = 4
	img_array[img_array==10] = 4
	img_array[img_array!=4] = 0.0 #Sets all other labels other than LA label to zero
	img_nifti = nib.Nifti1Image(img_array, img.affine)

	return img_nifti

def Get_LA_ONLY_label(Path2Img):

	"""
	Retrieves LA bloodpool labels.
	Use for constructing LA chamber mesh without PVs and LAA. 
	"""

	img = nib.load(Path2Img)
	img_array = img.get_fdata()
	img_array[img_array!=4] = 0.0 #Sets all other labels other than LA label to zero
	img_nifti = nib.Nifti1Image(img_array, img.affine)
	return img_nifti

def Get_RV_BP_label(Path2Img):
    
	"""
	Retrieves RV bloodpool label. 
	"""

	img = nib.load(Path2Img)
	img_array = img.get_fdata()
	img_array[img_array!=3] = 0.0 #Sets all other labels other than LV BP label to zero
	img_nifti = nib.Nifti1Image(img_array, img.affine)

	return img_nifti

def Get_RA_BP_label(Path2Img):
    
	"""
	Retrieves RV bloodpool label. 
	"""

	img = nib.load(Path2Img)
	img_array = img.get_fdata()
	img_array[img_array!=5] = 0.0 #Sets all other labels other than LV BP label to zero
	img_nifti = nib.Nifti1Image(img_array, img.affine)

	return img_nifti

def Get_PA_label(Path2Img):
    
	"""
	Retrieves RV bloodpool label. 
	"""

	img = nib.load(Path2Img)
	img_array = img.get_fdata()
	img_array[img_array!=7] = 0.0 #Sets all other labels other than LV BP label to zero
	img_nifti = nib.Nifti1Image(img_array, img.affine)

	return img_nifti

def All_except_LA(Path2Img):
	"""
	Retrieves 4-chamber segmentation omitting the LA and PVs & LAA
	"""

	img = nib.load(Path2Img)
	img_array = img.get_fdata()
	img_array[img_array==4] = 0.0
	img_array[img_array==8] = 0.0
	img_array[img_array==9] = 0.0	
	img_array[img_array==10] = 0.0

	for i in [1, 2, 3, 5, 6, 7]:
		img_array[img_array==i] = 1.0

	img_nifti = nib.Nifti1Image(img_array, img.affine)

	return img_nifti

def All_except_LA_multilabel(Path2Img):
	"""
	Retrieves 4-chamber segmentation omitting the LA and PVs & LAA
	"""

	img = nib.load(Path2Img)
	img_array = img.get_fdata()
	img_array[img_array==4] = 0.0
	img_array[img_array==8] = 0.0
	img_array[img_array==9] = 0.0	
	img_array[img_array==10] = 0.0
		
	img_nifti = nib.Nifti1Image(img_array, img.affine)

	return img_nifti

def Retrieve_label(Path2Img, label_num):
	"""
	Retrieves given label number
	"""

	img = nib.load(Path2Img)
	img_array = img.get_fdata()
	img_array[img_array!=label_num] = 0.0 #Sets all other labels other than LV BP label to zero
	img_nifti = nib.Nifti1Image(img_array, img.affine)

	return img_nifti

if __name__ == "__main__":

	path = sys.argv[1]
	label = sys.argv[2]
	# save_ind = sys.argv[3] 		# if saving segmentation from a later frame

	print(f"Extracting label {label} from: {path}")

	if label=="la_only":
		LA_ch = Get_LA_ONLY_label(path)
		print("Saving ... ")
		nib.save(LA_ch, f"{os.path.dirname(path)}/LA_chamber.nii")
	elif label=="la":
		LA = Get_LA_label(path)
		print("Saving ... ")
		nib.save(LA, f"{os.path.dirname(path)}/LA.nii")
	elif label=="lv":
		LV_BP = Get_LV_BP_label(path)
		print("Saving ... ")
		nib.save(LV_BP, f"{os.path.dirname(path)}/LV_BP.nii")
	elif label=="lv_myo": 
		LV_Myo = Get_LV_MYO_label(path)
		print("Saving ... ")
		nib.save(LV_Myo, f"{os.path.dirname(path)}/LV_Myo.nii")
	elif label=="lv_bp_myo":
		LV_BP_Myo = Get_LV_BP_MYO_label(path)
		print("Saving ... ")
		nib.save(LV_BP_Myo, f"{os.path.dirname(path)}/LV_BP_Myo.nii")
	elif label=="rv_bp":
		RV = Get_RV_BP_label(path)
		print("Saving ... ")
		nib.save(RV, f"{os.path.dirname(path)}/RV_{save_ind}.nii")
	elif label=="ra":
		RA = Get_RA_BP_label(path)
		print("Saving ... ")
		nib.save(RA, f"{os.path.dirname(path)}/RA.nii")
	elif label=="pa":
		PA = Get_PA_label(path)
		print("Saving ... ")
		nib.save(PA, f"{os.path.dirname(path)}/PA.nii")
	elif label=="all_excl_la":
		heart_exc_LA = All_except_LA_multilabel(path)
		print("Saving ... ")
		nib.save(heart_exc_LA, f"{os.path.dirname(path)}/Heart_excl_LA_multilabel.nii")
	else:
		print("2nd argument needs to be one of the optional labels!!!")

	# for i in range(1, 11):
	# 	img = Retrieve_label(path, i)
	# 	print("Saving label ", i)
	# 	nib.save(img, f"{os.path.dirname(path)}/label-{i}.nii")