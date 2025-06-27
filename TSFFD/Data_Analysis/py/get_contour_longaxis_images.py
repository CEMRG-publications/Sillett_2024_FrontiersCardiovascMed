"""
Use this script to generate 2D strains from the extracted, 2D 4CH and 2CH images.
"""

from vtk import * 
import argparse
import numpy as np
from xml.dom.minidom import parse
import matplotlib.pyplot as plt
import SimpleITK as sitk
from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get the contours of a 3d mesh at a \
                                     plane that is given by mps file (min 3 points)')
    parser.add_argument('--longaxis-img', required=True, help='Long axis extracted 2D image.')
    parser.add_argument('--filepath', required=True, help='Project directory with all the files', default='./')
    parser.add_argument('--basename', help='basename for all the files eg. transformed-', 
                        default='transformed-')
    parser.add_argument('--numTimes', help='Total number of time frames [10]', default=10)
    parser.add_argument('--contourFile', help='basename for output contour files eg. 4ch_contour-{time}.vtk',\
                        default='4ch_contour-clip-')    
    parser.add_argument('--png_out', help='output png filename', default='4chamber_long_strain-clip.png')
    parser.add_argument('--file-type', help='Filetype of VTK files', default='.vtk')
    parser.add_argument('--flip', action='store_true')
    
    args = parser.parse_args()

    numTimes = int(args.numTimes)

    # Read in initial mesh
    path2init_msh=f"{args.filepath}/{args.basename}0{args.file_type}"
    # reader=vtkXMLPolyDataReader();
    # reader=vtkXMLUnstructuredGridReader();
    reader=vtkPolyDataReader();
    reader.SetFileName(path2init_msh)
    reader.Update()
    geomFilter=vtkGeometryFilter()
    geomFilter.SetInputConnection(reader.GetOutputPort())
    geomFilter.Update()
    refLA = geomFilter.GetOutput()
    # print(refLA)

    # Read in extracted 2D long axis view image
    path2img_pl=Path(args.longaxis_img)
    img=sitk.ReadImage(args.longaxis_img)

    # Extract origin and normal from extracted 2 long axis image
    origin=img.GetOrigin()
    # print(type(origin))
    origin=np.array([origin[0], origin[1], 0])
    normal=np.array([0, 0, 1])  # 4CH

    # Define cutter to create contour
    ## Contour
    plane=vtkPlane()
    plane.SetOrigin(origin)
    plane.SetNormal(normal)                
    inputMapper=vtkPolyDataMapper()
    # inputMapper.SetInputData(refLA);    
    cutter=vtkCutter()
    cutter.SetCutFunction(plane);
    cutter.SetInputData(refLA);    
    cutter.GenerateValues(1, 0, 0); # (#contours, min distance, max distance)
    cutter.Update()

    # Cut and measure contour legnths across all time frames
    contour_len=np.zeros(numTimes)

    for time in range (0, numTimes): 
        # Meshtool resample surfmesh outputs unstructured grid format which 
        # gets carried through with the MIRTK transform points code

        # Load LA at each- time point
        LAN_file=f'{args.filepath}/{args.basename}{str(time)}{args.file_type}'
        contourFilename = args.contourFile + str(time) + args.file_type
        contourFilename = args.contourFile + str(time) + '.vtk'
        # reader=vtkXMLPolyDataReader();
        # reader=vtkUnstructuredGridReader();
        reader=vtkPolyDataReader();
        reader.SetFileName(LAN_file)
        reader.Update()
        geomFilter=vtkGeometryFilter()
        geomFilter.SetInputConnection(reader.GetOutputPort())
        geomFilter.Update()
        LA = geomFilter.GetOutput()
        
        # Cut LAN msh
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
        writer.SetFileName(f"{args.filepath}/{contourFilename}")
        writer.SetFileVersion(42)
        writer.Write()

    # Calculate strain
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
    
    fig.savefig(f'{args.filepath}/{args.png_out}', dpi = (200))

    ## Save txt file of reservoir strain
    # print(contour_len)
    max_contour_len=np.max(contour_len)
    min_contour_len=np.min(contour_len)

    res_strain = (max_contour_len-min_contour_len)/min_contour_len * 100
    print("Reservoir strain: ", res_strain)

    # Save 2D strain transient and reservoir strain
    np.savetxt(f'{args.filepath}/4chamber_strain_transient-clip.txt', contour_len, fmt="%g")
    np.savetxt(f'{args.filepath}/4chamber_reservoir_strain-clip.txt', np.array([res_strain]), fmt="%g")