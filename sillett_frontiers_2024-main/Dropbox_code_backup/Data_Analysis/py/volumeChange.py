# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 15:02:44 2022

@author: Angela Lee
"""
import numpy as np
from xml.dom import minidom
from vtk import * 
from vtk.util import numpy_support
import matplotlib.pyplot as plt
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get the change in volume of the surface cavity')

    parser.add_argument('-filepath',
                        help='Project directory with all the files', default='./')
    parser.add_argument('-basename', help='basename for all the files eg. transformed-.vtk', 
                        default='transformed-')
    parser.add_argument('-filetype', help='Filetype of vtk files', default='.vtk')
    parser.add_argument('-numTimes', help='Number of time frames [25]', default=25)
    parser.add_argument('-skipTime', help='every nth frame [1]', default=1)
    
    args = parser.parse_args()

    # LA_files=r"D:/Dropbox/Work/Atria/Stanford/data/case006/2_motion"
    # LA0_file=LA_files + r"/transformed-0.vtk"
    # numTimes=24 -#25; 
    LA_files=args.filepath
    LA0_file=LA_files + args.basename + '1' + args.filetype
    numTimes=int(args.numTimes)
    skipTime=int(args.skipTime)

    reader=vtkPolyDataReader();
    reader.SetFileName(LA0_file)
    reader.Update()
    geomFilter=vtkGeometryFilter()
    geomFilter.SetInputConnection(reader.GetOutputPort())
    geomFilter.Update()
    refLA = geomFilter.GetOutput()
    areaChangeArray=np.zeros(refLA.GetNumberOfCells())

    globalVolume=np.zeros(int(numTimes/skipTime))
    globalSA=np.zeros(int(numTimes/skipTime))
    j=0
    normTime=np.zeros(int(numTimes/skipTime))
    #Loop frames: 25 frames in cine
    for time in range (1, numTimes, skipTime): 
        # Meshtool resample surfmesh outputs unstructured grid format which 
        # gets carried through with the MIRTK transform points code
        # Load LA at each- time point
        LAN_file=LA_files + args.basename + str(time) + args.filetype
        print(LAN_file)
        
        reader=vtkPolyDataReader();
        reader.SetFileName(LAN_file)
        reader.Update()
        geomFilter=vtkGeometryFilter()
        geomFilter.SetInputConnection(reader.GetOutputPort())
        geomFilter.Update()
        LA = geomFilter.GetOutput()
        
        massProperties = vtkMassProperties()
        massProperties.SetInputData(LA)
        globalVolume[j]=massProperties.GetVolume()/1000
        globalSA[j]=massProperties.GetSurfaceArea()
        normTime[j]=time/numTimes
        j+=1
        
    plt.plot(normTime,globalVolume)
    plt.xlabel('Time (normalised)')
    plt.ylabel('LA blood pool volume (ml)')
    plt.show()
    
    
    