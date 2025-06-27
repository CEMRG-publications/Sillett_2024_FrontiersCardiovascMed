# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 15:02:44 2022

@author: Angela Lee

Amended for .vtp files
"""

import numpy as np
from vtk import * 
from vtk.util import numpy_support
import matplotlib.pyplot as plt
import argparse

if __name__ == '__main__':
	# parse command line arguments
    parser = argparse.ArgumentParser(description='Get the change in volume of the surface cavity')

    parser.add_argument('--filepath', required=True,
                        help='Project directory with all the files', default='./')
    parser.add_argument('--basename', required=True, help='basename for all the files eg. transformed-', 
                        default='transformed-')
    parser.add_argument('--filetype', required=True, help='Filetype of vtk files', default='.vtk')
    parser.add_argument('--numTimes', required=True, help='Number of time frames [25]', default=25)
    parser.add_argument('--skipTime', help='every nth frame [1]', default=1)
    parser.add_argument('--save', help='Only give argument if want to save. Leave blank if do not want to save')
    
    args = parser.parse_args()

    LA_files=args.filepath
    LA0_file=LA_files + args.basename + '0' + args.filetype ## initial LA msh
    numTimes=int(args.numTimes)
    skipTime=int(args.skipTime)

    reader=vtkXMLPolyDataReader();
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
    for time in range (0, numTimes, skipTime): 
        # Meshtool resample surfmesh outputs unstructured grid format which 
        # gets carried through with the MIRTK transform points code
        # Load LA at each- time point
        LAN_file=LA_files + args.basename + str(time) + args.filetype
        print(LAN_file)
        
        reader=vtkXMLPolyDataReader();
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

    if args.save:
    	print("Saving!")

    	plt.savefig(f"{args.filepath}/{args.basename}vol.png", bbox_inches='tight')
    else:
    	print("Not saving!")

    plt.show()
    

    