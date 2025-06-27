"""
Use this script to read in .vtu files using vtk, then re-write them as vtk files with specified version.

This should enable the meshes to be read in by the CemrgApp Demo Tracking button.
"""

from pathlib import Path
from vtk import *
import sys

path2msh=sys.argv[1]
path2msh_pl = Path(path2msh)

print("HERE")

# Set type of reader
reader=vtkXMLUnstructuredGridReader()
# reader=vtkUnstructuredGridReader()
# reader=vtkPolyDataReader()
# reader=vtkXMLPolyDataReader()

reader.SetFileName(path2msh)
reader.Update()
geomFilter=vtkGeometryFilter()
geomFilter.SetInputConnection(reader.GetOutputPort())
geomFilter.Update()
refLA = geomFilter.GetOutput()
num_cells = refLA.GetNumberOfCells()
print(num_cells)

if num_cells != 0:
    print("Num cells != 0")
    print("Saving")
    writer = vtkPolyDataWriter()
    # writer = vtkXMLUnstructuredGridWriter()
    writer.SetFileTypeToASCII()        
    writer.SetInputData(refLA)

    # Set name of saved files
    # writer.SetFileName(f"{path2msh_pl.parent}/{path2msh_pl.stem}-save.vtk")
    writer.SetFileName(f"{path2msh_pl.parent}/{path2msh_pl.stem}.vtk")
    # writer.SetFileName(f"{path2msh_pl.parent}/transformed-{path2msh_pl.stem[-1]}.vtk")
    # writer.SetFileName(f"{path2msh_pl.parent.parent.parent}/demo_tracking/transformed-{path2msh_pl.stem[-1]}.vtk")

    writer.SetFileVersion(42)
    writer.Write()
else:
    print("No cells found")