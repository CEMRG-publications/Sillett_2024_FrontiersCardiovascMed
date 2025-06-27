# -*- coding: utf-8 -*-
"""
Rotate mesh to long axis and get the contour 

amended.

This script differs from get_contour.py as it doesn't caclulate any strains,
it just prints ou the calculated Normal and Origin vecotrs.

"""

from vtk import * 
import argparse
import numpy as np
from xml.dom.minidom import parse
import sys
#from vedo import *
#import pyvista
import matplotlib.pyplot as plt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get the contours of a 3d mesh at a \
                                     plane that is given by mps file (min 3 points)')
    parser.add_argument('--mpsfile', required=True, help='mps landmarks file (we take the 1st 3 points to make a plane)')
    parser.add_argument('--filepath',
                        help='Project directory with all the files', default='./')
    parser.add_argument('--basename', help='basename for all the files eg. transformed-', 
                        default='transformed-')
    parser.add_argument('--numTimes', help='Total number of time frames [10]', default=10)
    parser.add_argument('--contourFile', help='basename for output contour files eg. 4ch_contour-{time}.vtk',\
                        default='4ch_contour-')    
    parser.add_argument('--png_out', help='output png filename', default='./long_strain.png')
    parser.add_argument('--file-type', help='Filetype of VTK files', default='.vtk')
    parser.add_argument('--flip', action='store_true')              
    
    args = parser.parse_args()
    
    numTimes = int(args.numTimes)
    
    # Read in LA at t=0 
    LA0_file=f"{args.filepath}/{args.basename}0-clip{args.file_type}"
    # reader=vtkXMLPolyDataReader();
    reader=vtkXMLUnstructuredGridReader();
    # reader=vtkPolyDataReader();
    reader.SetFileName(LA0_file)
    reader.Update()
    geomFilter=vtkGeometryFilter()
    geomFilter.SetInputConnection(reader.GetOutputPort())
    geomFilter.Update()
    refLA = geomFilter.GetOutput()
    # print(refLA)
    
    ## Read in mps file for LM at long axis slices (4ch_LA.mps)
    ## Read in landmarks to define 3D plane
    LM_mps=args.mpsfile
    # mpsfile=/data/Dropbox/Work/Atria/GSTT/data/case001/1_seg/4ch_LA.mps
    # Read in long axis LM mps 
    dom1=parse(LM_mps)
    xlist=dom1.getElementsByTagName("x")    
    ylist=dom1.getElementsByTagName("y")    
    zlist=dom1.getElementsByTagName("z")    
    
    LM1=np.zeros(3); 
    LM2=np.zeros(3); 
    LM3=np.zeros(3); 
    LM1[0]=xlist[0].firstChild.data
    LM1[1]=ylist[0].firstChild.data
    LM1[2]=zlist[0].firstChild.data
    
    LM2[0]=xlist[1].firstChild.data
    LM2[1]=ylist[1].firstChild.data
    LM2[2]=zlist[1].firstChild.data
    
    LM3[0]=xlist[2].firstChild.data    
    LM3[1]=ylist[2].firstChild.data
    LM3[2]=zlist[2].firstChild.data

    # Flip x,y for LM data points if reading in transformed-X.vtk meshes 
    if args.flip:
        LM1[0]=-LM1[0]
        LM2[0]=-LM2[0]
        LM3[0]=-LM3[0]
        LM1[1]=-LM1[1]
        LM2[1]=-LM2[1]
        LM3[1]=-LM3[1]

    transform=np.eye(4)
    transform[0:3,3]=-LM1 # Move to first LM point as zero 
   
    # set up vectors created by landmarks
    LMa=(LM2-LM1)/np.linalg.norm(LM2-LM1)
    LMb=(LM3-LM1)/np.linalg.norm(LM3-LM1)
    # Check that the 2 vectors aren't colinear, if so - then move to next point
    tol=1e-2
    i=3
    while np.linalg.norm(LMa-LMb)<tol:
        LM3[0]=xlist[i].firstChild.data    
        LM3[1]=ylist[i].firstChild.data
        LM3[2]=zlist[i].firstChild.data
        LMb=(LM3-LM1)/np.linalg.norm(LM3-LM1)    
        i+=1
        if i>=xlist.length:
            print("Landmark file needs 3 points that define 2 vectors that are not co-linear.")
            sys.exit()
            
    LM_2=np.cross(LMa, LMb)
    LM_2=LM_2/np.linalg.norm(LM_2); # normalised vector that is perpendicular to 4ch long axis slice    

    ## Contour
    plane=vtkPlane()
    plane.SetOrigin(LM3)
    plane.SetNormal(LM_2)                
    inputMapper=vtkPolyDataMapper()
    # inputMapper.SetInputData(refLA);    
    cutter=vtkCutter()
    cutter.SetCutFunction(plane);
    cutter.SetInputData(refLA);    
    cutter.GenerateValues(1, 0, 0); # (#contours, min distance, max distance)
    cutter.Update()

    ## Print plane properties
    print(f"Origin: {LM3[0]}, {LM3[1]}, {LM3[2]}")
    print(f"Normal: {LM_2[0]}, {LM_2[1]}, {LM_2[2]}")
    
    contour_len=np.zeros(numTimes)

    for time in range (0, numTimes): 
        # Meshtool resample surfmesh outputs unstructured grid format which 
        # gets carried through with the MIRTK transform points code
        # Load LA at each- time point
        LAN_file=f'{args.filepath}/{args.basename}{str(time)}-clip{args.file_type}'
        contourFilename = args.contourFile + str(time) + args.file_type
        contourFilename = args.contourFile + str(time) + '.vtk'
        # reader=vtkXMLPolyDataReader();
        reader=vtkXMLUnstructuredGridReader();
        # reader=vtkPolyDataReader();
        reader.SetFileName(LAN_file)
        reader.Update()
        geomFilter=vtkGeometryFilter()
        geomFilter.SetInputConnection(reader.GetOutputPort())
        geomFilter.Update()
        LA = geomFilter.GetOutput()
        
        # Update input 
        cutter.SetInputData(LA);    
        cutter.Update()
        contour=cutter.GetOutput()

        contour_len[time]=cutter.GetOutput().GetLength()
        print(cutter.GetOutput().GetLength())    
        
        ## If we want to have the contours overlaid on the transformed.vtk meshes,
        ## set flip as false here (do not flip back into image space)
        args.flip=False        
        
        # Flip the points back to image space
        for ptID in range (0, contour.GetNumberOfPoints()):
            point=np.zeros(4)    
            # Flip the ref polydata - if transformed-X.vtk - then set as true
            if args.flip: # If flip flag is set as true (Needed for MIRTK mesh processing)
                point[0] = -contour.GetPoint(ptID)[0];
                point[1] = -contour.GetPoint(ptID)[1];
            else:
                point[0] = contour.GetPoint(ptID)[0];
                point[1] = contour.GetPoint(ptID)[1];
            point[2] = contour.GetPoint(ptID)[2];
            point[3] = 1;        
            contour.GetPoints().SetPoint(ptID, point[0:3])
            
        writer = vtkPolyDataWriter()
        # writer = vtkXMLUnstructuredGridWriter()
        writer.SetFileTypeToASCII()        
        writer.SetInputData(contour)
        writer.SetFileName(contourFilename)
        # writer.SetFileVersion(42)
        # writer.Write()
    
    normTime=np.arange(0,numTimes)/numTimes 
    strain=100*(contour_len-contour_len[0])/contour_len[0]  ## strain calculated using contour length
    
    fig, (ax1, ax2) = plt.subplots(2,1,figsize=(7, 9))
    
    ax1.plot(normTime,strain)
    ax1.set_title('Longitudinal Strain')
    ax1.set(xlabel='Time (normalised)')
    ax1.set(ylabel='longitudinal strain')
    ax1.label_outer()
    
    SR = np.gradient(strain, normTime)
    ax2.plot(normTime,SR)
    ax2.set_title('Strain Rate')
    ax2.set(xlabel='Time (normalised)')
    ax2.set(ylabel='longitudinal strain rate')
    
    ax1.grid(True)
    ax2.grid(True)
    
    # fig.savefig(args.png_out, dpi = (200))
    
    #plt.show()
    # # # Visualise contour
    # Below code visualises the contour cut slice of mesh.
    # cutterMapper=vtkPolyDataMapper()        
    # cutterMapper.SetInputConnection(cutter.GetOutputPort());
    # cutterMapper.ScalarVisibilityOff();
    
    # colors=vtkNamedColors()
    # planeActor=vtkActor()
    # planeActor.GetProperty().SetColor(colors.GetColor3d("Deep_pink"));
    # planeActor.GetProperty().SetLineWidth(5);
    # planeActor.SetMapper(cutterMapper);
    
    # inputActor=vtkActor()
    # inputActor.GetProperty().SetColor(colors.GetColor3d("Bisque"));
    # inputActor.SetMapper(inputMapper);

    # # Create renderers and add actors of plane and cube
    # renderer=vtkRenderer();
    # renderer.AddActor(planeActor); # display the rectangle resulting from the
    #                             # cut
    # renderer.AddActor(inputActor); # display the cube

    # # Add renderer to renderwindow and render
    # renderWindow=vtkRenderWindow()
    # renderWindow.AddRenderer(renderer);
    # renderWindow.SetWindowName("ContoursFromPolyData");
    # renderWindow.SetSize(600, 600);
    
    # interactor=vtkRenderWindowInteractor()
    # interactor.SetRenderWindow(renderWindow);
    # renderer.SetBackground(colors.GetColor3d("Slate_grey"));
    # renderWindow.Render();
    
    # interactor.Start();

#    print(contour.GetLength())
