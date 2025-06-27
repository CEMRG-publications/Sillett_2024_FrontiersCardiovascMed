"""
Use this script to read in .vtu files using vtk, then re-write them as vtk files with specified version.

This should enable the meshes to be read in by the CemrgApp Demo Tracking button.
"""

from pathlib import Path
from vtk import *
# import sys


numTimes=10

for i in range(0, numTimes):
    path2msh=f"/home/csi20local/Data/RG_CT_Cases/CT-CRT/case01/MT-HiRes/SW-0.0-BE-1e-9/transformed-{i}-clip.vtu"
    path2msh_pl = Path(path2msh)

    reader=vtkXMLUnstructuredGridReader()
    reader.SetFileName(path2msh)
    reader.Update()
    geomFilter=vtkGeometryFilter()
    geomFilter.SetInputConnection(reader.GetOutputPort())
    geomFilter.Update()
    refLA = geomFilter.GetOutput()
    
    writer = vtkPolyDataWriter()
    # writer = vtkXMLUnstructuredGridWriter()
    writer.SetFileTypeToASCII()        
    writer.SetInputData(refLA)
    writer.SetFileName(f"{path2msh_pl.parent}/{path2msh_pl.stem[:-5]}.vtk")
    writer.SetFileVersion(42)
    writer.Write()