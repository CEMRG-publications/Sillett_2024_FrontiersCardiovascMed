#include <vtkActor.h>
#include <vtkCamera.h>
#include <vtkNamedColors.h>
#include <vtkPolyDataMapper.h>
#include <vtkProperty.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkSmartPointer.h>
#include <vtkXMLPolyDataReader.h>
#include <vtkPNGWriter.h>                 //new
#include <vtkWindowToImageFilter.h>       //new
#include <vtkVersion.h>                   //new
#include <vtkPolyData.h>                  //new
#include <vtkLight.h>                     //new
#include <vtkLightCollection.h>           //new

#include <vtksys/SystemTools.hxx>
#include "vtkPolyDataReader.h"

#include <vtkPolyDataNormals.h>
#include <vtkDataArray.h>
#include <vtkDoubleArray.h>
#include <vtkFloatArray.h>
#include <vtkCellData.h>

#include <vtkCellCenters.h>
#include <vtkDataSetMapper.h>

#include <vtkXMLUnstructuredGridReader.h>
#include <vtkDataSetSurfaceFilter.h>
#include <vtkUnstructuredGrid.h>

using namespace std;

namespace
{
  vtkSmartPointer<vtkPolyData> ReadMesh( const char* filename );
}

void printarraydouble (double arg[], int length)
{
  for (int n=0; n<length; ++n)
    cout << arg[n] << ' ';
  cout << '\n';
}

void printarrayint (int arg[], int length)
{
  for (int n=0; n<length; ++n)
    cout << arg[n] << ' ';
  cout << '\n';
}

int main(int argc, char* argv[])
{
  // Parse command line arguments
  if (argc != 2)
  {
    std::cerr << "Usage: " << argv[0] << " Mesh(.vtp) e.g. Torso.vtp"
              << std::endl;
    return EXIT_FAILURE;
  }

  // New way assigning filename
  const char *file1 = 0;
  if (argc > 1)
  {
    file1 = argv[1];
  }

  // Load PolyData Mesh
  vtkSmartPointer<vtkPolyData> pd;
  pd = ReadMesh(file1);

  cout << "Number of Cells: " << pd->GetNumberOfCells() << endl;


  for(vtkIdType cellID = 0; cellID < pd->GetNumberOfCells(); cellID++)
  {
    vtkCell* cell = pd->GetCell(cellID);
    vtkIdList* pointIdList = cell->GetPointIds();

    double points[3][3];

    for(vtkIdType pointID = 0; pointID < pointIdList->GetNumberOfIds(); pointID++)
    {
      // cout << pointID << endl;

      // cout <<  "Cell " << cellID << " Point " << pointIdList->GetId(pointID) << " ";

      cell->GetPoints()->GetPoint(pointID, points[pointID]);
      // cout << " " << points[pointID][0] << " " << points[pointID][1] << " " << points[pointID][2] << endl;
    }

    double v1[3] = {points[0][0] - points[1][0], points[0][1] - points[1][1], points[0][2] - points[1][2]};
    double v2[3] = {points[0][0] - points[2][0], points[0][1] - points[2][1], points[0][2] - points[2][2]};
    double v3[3] = {points[1][0] - points[2][0], points[1][1] - points[2][1], points[1][2] - points[2][2]};

    // printarraydouble(v1, 3);

    double l1;
    double l2;
    double l3;

    l1 = pow(v1[0], 2.0) + pow(v1[1], 2.0) + pow(v1[2], 2.0);
    l1 = pow(l1, 0.5);

    l2 = pow(v2[0], 2.0) + pow(v2[1], 2.0) + pow(v2[2], 2.0);
    l2 = pow(l2, 0.5);

    l3 = pow(v3[0], 2.0) + pow(v3[1], 2.0) + pow(v3[2], 2.0);
    l3 = pow(l3, 0.5);

    // printarraydouble(l1, 3);

    double frac = (l1 + l2 + l3)/2.0;
    double x = frac - l1;
    double y = frac - l2;
    double z = frac - l3;

    double cellArea = frac*x*y*z;
    cellArea = pow(cellArea, 0.5);

    cout << "Cell " << cellID << " Area " << cellArea << endl;
  }

  return EXIT_SUCCESS;
}

namespace
{
  vtkSmartPointer<vtkPolyData> ReadMesh( const char* filename )
  {
    vtkSmartPointer<vtkPolyData> polydata;

    // Get file extension
    std::string extension = vtksys::SystemTools::GetFilenameLastExtension(std::string(filename));

    // Drop the case of the extension
    std::transform(extension.begin(), extension.end(), extension.begin(), ::tolower);

    if (extension == ".vtp")
    {
      vtkSmartPointer<vtkXMLPolyDataReader> PolyDatareader = vtkSmartPointer<vtkXMLPolyDataReader>::New();
      PolyDatareader->SetFileName(filename);
      PolyDatareader->Update();
      polydata = PolyDatareader->GetOutput();
    }

    if (extension == ".vtu")
    {
      auto UnstructGridreader = vtkSmartPointer<vtkXMLUnstructuredGridReader>::New();
      UnstructGridreader->SetFileName (filename);
      UnstructGridreader->Update();

      vtkSmartPointer<vtkUnstructuredGrid> pdTrackedUnstructGrid;
      pdTrackedUnstructGrid = UnstructGridreader->GetOutput();

      vtkSmartPointer<vtkDataSetSurfaceFilter> surfaceFilter = vtkSmartPointer<vtkDataSetSurfaceFilter>::New();
      surfaceFilter->SetInputData(pdTrackedUnstructGrid);
      surfaceFilter->Update();

      polydata = surfaceFilter->GetOutput();
    }

    else if (extension == ".vtk")
    {
      auto PolyDatareader = vtkSmartPointer<vtkPolyDataReader>::New();
      PolyDatareader->SetFileName (filename);
      PolyDatareader->Update();
      polydata = PolyDatareader->GetOutput();
    }

    return polydata;
  }
}
