"""
Use this file to rotate a mesh by 180 and 180 in X and Y respectively
"""

import sys
import pyvista as pv
from pathlib import Path

path2msh=sys.argv[1]

msh=pv.read(path2msh)

# Rotate 180 degrees in the X direction
msh.rotate_x(180)

# Rotate 180 degrees in the Y direction
msh.rotate_y(180)

# save
path2msh_pl=Path(path2msh)
msh.save(f"{path2msh_pl.parent}/{path2msh_pl.stem}-rot.vtk")