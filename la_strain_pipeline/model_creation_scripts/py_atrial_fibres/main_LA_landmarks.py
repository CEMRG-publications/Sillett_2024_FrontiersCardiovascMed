import os
import sys

# from py_atrial_fibres.json_utils import *
# from py_atrial_fibres.meshtools_utils import *
# from py_atrial_fibres.UAC_surface_utils import *

from json_utils import *
from meshtools_utils import *
from UAC_surface_utils import *


def get_mv_clipper_vtk(meshfolder, mv_clipper_vtk):
    prodSeedLabels=meshfolder+"/prodSeedLabels.txt"
    prodSeedIds=meshfolder+"/prodSeedIds.txt"
    with open(prodSeedLabels) as Labels, open(prodSeedIds) as Ids:
        for x, y in zip(Labels, Ids):
            if x.strip()=="21": # MV label
                mv_clipper_init=meshfolder+"/pvClipper_"+y.strip()+".vtk"
    os.rename(mv_clipper_init, meshfolder+"/"+mv_clipper_vtk)

def main():

    meshfolder = sys.argv[1] + "/"

    meshname = sys.argv[2]
    mv_clipper_vtk = sys.argv[3]

    if not os.path.exists(meshfolder+"/"+mv_clipper_vtk):
        get_mv_clipper_vtk(meshfolder, mv_clipper_vtk)

    input_tags = load_json('/home/csi20/Projects_Local/py_atria_latest/py_atria-main/py_atrial_fibres/input_tags_setup.json')

    extract_boundaries(meshfolder,meshname,
                       mv_clipper_vtk,
                       input_tags)

if __name__ == '__main__':
    main()
