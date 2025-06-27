## Failed attempt to use pyvista/vtk to automate movie making for moving msh/overalid on image
##

import pyvista as pv
from vtk import *

## initialise plotter

plotter = pv.Plotter()

## Read in nii image
reader = vtkNIFTIImageReader()
reader.SetFileName("/home/csi20local/Dropbox/phd/Data/RG_CT_Cases/CT-CRT-07/dcm-0.nii")
reader.Update()
image = reader.GetOutput()

##
mapper = vtkImageMapper3D()
mapper.SetInputData(image)
img_actor = vtkImageActor()
img_actor.SetMapper(mapper)


# # img_actor = vtkImageActor()
# img_actor.GetMapper().SetInputConnection(reader.GetOutputPort())
# img_actor.SetDisplayExtent(0, 0, 50, 50, 0, 0)

# plotter.add_actor(img_actor)
# print(type(img_actor))

# image = reader.GetOutput()
# print(type(image))

# plotter.show()